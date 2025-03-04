# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import api, models
from odoo.tools import float_is_zero, float_round, format_datetime


class ReplenishReportRepairLine(models.AbstractModel):
    _name = "report.repair_line_forecasted_qty.replenish_report_repair_line"
    _description = "Stock Replenishment Report"

    def _product_domain(self, product_id):
        return [("product_id", "=", product_id)]

    def _move_domain(self, product_id, wh_location_ids):
        move_domain = self._product_domain(product_id)
        move_domain += [("product_uom_qty", "!=", 0)]
        out_domain = move_domain + [
            "&",
            ("location_id", "in", wh_location_ids),
            ("location_dest_id", "not in", wh_location_ids),
        ]
        in_domain = move_domain + [
            "&",
            ("location_id", "not in", wh_location_ids),
            ("location_dest_id", "in", wh_location_ids),
        ]
        return in_domain, out_domain

    def _move_draft_domain(self, product_id, wh_location_ids):
        in_domain, out_domain = self._move_domain(product_id, wh_location_ids)
        in_domain += [("state", "=", "draft")]
        out_domain += [("state", "=", "draft")]
        return in_domain, out_domain

    def _move_confirmed_domain(self, product_id, wh_location_ids):
        in_domain, out_domain = self._move_domain(product_id, wh_location_ids)
        out_domain += [("state", "not in", ["draft", "cancel", "done"])]
        in_domain += [("state", "not in", ["draft", "cancel", "done"])]
        return in_domain, out_domain

    def _compute_draft_quantity_count(self, product_id, wh_location_ids):
        in_domain, out_domain = self._move_draft_domain(product_id, wh_location_ids)
        incoming_moves = self.env["stock.move"].read_group(
            in_domain, ["product_qty:sum"], "product_id"
        )
        outgoing_moves = self.env["stock.move"].read_group(
            out_domain, ["product_qty:sum"], "product_id"
        )
        in_sum = sum(move["product_qty"] for move in incoming_moves)
        out_sum = sum(move["product_qty"] for move in outgoing_moves)
        return {
            "draft_picking_qty": {"in": in_sum, "out": out_sum},
            "qty": {"in": in_sum, "out": out_sum},
        }

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            "data": data,
            "doc_ids": docids,
            "doc_model": "repair.line",
            "docs": self._get_report_data(repair_line_ids=docids),
        }

    def _get_report_data(self, repair_line_ids):
        res = {}

        # Get the warehouse we're working on as well as its locations.
        if self.env.context.get("warehouse"):
            warehouse = self.env["stock.warehouse"].browse(
                self.env.context["warehouse"]
            )
        else:
            warehouse = self.env["stock.warehouse"].search(
                [("company_id", "=", self.env.company.id)], limit=1
            )
            self.env.context = dict(self.env.context, warehouse=warehouse.id)
        wh_location_ids = [
            loc["id"]
            for loc in self.env["stock.location"].search_read(
                [("id", "child_of", warehouse.view_location_id.id)],
                ["id"],
            )
        ]
        res["active_warehouse"] = warehouse.display_name
        product_id = False
        repair_lines = self.env["repair.line"].browse(repair_line_ids)
        for repair_line in repair_lines:
            res["product_templates"] = False
            res["product_variants"] = repair_line.product_id
            res["multiple_product"] = len(repair_line.product_id) > 1
            res["uom"] = repair_line.uom_id.display_name
            res["quantity_on_hand"] = repair_line.product_id.qty_available
            res["virtual_available"] = repair_line.virtual_available
            product_id = repair_line.product_id
        if product_id:
            res.update(self._compute_draft_quantity_count(product_id, wh_location_ids))
            res["lines"] = self._get_report_lines(product_id, wh_location_ids)
        return res

    def _prepare_report_line(
        self,
        quantity,
        move_out=None,
        move_in=None,
        replenishment_filled=True,
        product=False,
        reservation=False,
    ):
        timezone = self._context.get("tz")
        product = product or (move_out.product_id if move_out else move_in.product_id)
        is_late = move_out.date < move_in.date if (move_out and move_in) else False
        return {
            "document_in": move_in._get_source_document() if move_in else False,
            "document_out": move_out._get_source_document() if move_out else False,
            "product": {"id": product.id, "display_name": product.display_name},
            "replenishment_filled": replenishment_filled,
            "uom_id": product.uom_id,
            "receipt_date": format_datetime(
                self.env, move_in.date, timezone, dt_format=False
            )
            if move_in
            else False,
            "delivery_date": format_datetime(
                self.env, move_out.date, timezone, dt_format=False
            )
            if move_out
            else False,
            "is_late": is_late,
            "quantity": float_round(
                quantity, precision_rounding=product.uom_id.rounding
            ),
            "move_out": move_out,
            "move_in": move_in,
            "reservation": reservation,
        }

    def _get_report_lines(self, product_id, wh_location_ids):
        def _rollup_move_dests(move, seen):
            for dst in move.move_dest_ids:
                if dst.id not in seen:
                    seen.add(dst.id)
                    _rollup_move_dests(dst, seen)
            return seen

        def _reconcile_out_with_ins(
            lines, out, ins, demand, only_matching_move_dest=True
        ):
            index_to_remove = []
            for index, in_ in enumerate(ins):
                rounding = out.product_id.uom_id.rounding
                if float_is_zero(in_["qty"], precision_rounding=rounding):
                    continue
                if (
                    only_matching_move_dest
                    and in_["move_dests"]
                    and out.id not in in_["move_dests"]
                ):
                    continue
                taken_from_in = min(demand, in_["qty"])
                demand -= taken_from_in
                lines.append(
                    self._prepare_report_line(
                        taken_from_in, move_in=in_["move"], move_out=out
                    )
                )
                in_["qty"] -= taken_from_in
                if in_["qty"] <= 0:
                    index_to_remove.append(index)
                rounding = out.product_id.uom_id.rounding
                if float_is_zero(demand, precision_rounding=rounding):
                    break
            for index in index_to_remove[::-1]:
                ins.pop(index)
            return demand

        in_domain, out_domain = self._move_confirmed_domain(product_id, wh_location_ids)
        outs = self.env["stock.move"].search(
            out_domain, order="priority desc, date, id"
        )
        outs_per_product = defaultdict(lambda: [])
        outs_reservation = {}
        for out in outs:
            outs_per_product[out.product_id.id].append(out)
            outs_reservation[out.id] = out._get_orig_reserved_availability()
        ins = self.env["stock.move"].search(in_domain, order="priority desc, date, id")
        ins_per_product = defaultdict(lambda: [])
        for in_ in ins:
            ins_per_product[in_.product_id.id].append(
                {
                    "qty": in_.product_qty,
                    "move": in_,
                    "move_dests": _rollup_move_dests(in_, set()),
                }
            )
        currents = {
            c["id"]: c["qty_available"] for c in outs.product_id.read(["qty_available"])
        }

        lines = []
        for product in (ins | outs).product_id:
            for out in outs_per_product[product.id]:
                reserved_availability = outs_reservation[out.id]
                r = product.uom_id.rounding
                if float_is_zero(reserved_availability, precision_rounding=r):
                    continue
                current = currents[out.product_id.id]
                reserved = out.product_uom._compute_quantity(
                    reserved_availability, product.uom_id
                )
                currents[product.id] -= reserved
                lines.append(
                    self._prepare_report_line(reserved, move_out=out, reservation=True)
                )

            unreconciled_outs = []
            for out in outs_per_product[product.id]:
                reserved_availability = outs_reservation[out.id]
                # Reconcile with the current stock.
                current = currents[out.product_id.id]
                reserved = 0.0
                r = product.uom_id.rounding
                if not float_is_zero(reserved_availability, precision_rounding=r):
                    reserved = out.product_uom._compute_quantity(
                        reserved_availability, product.uom_id
                    )
                demand = out.product_qty - reserved
                taken_from_stock = min(demand, current)
                r = product.uom_id.rounding
                if not float_is_zero(taken_from_stock, precision_rounding=r):
                    currents[product.id] -= taken_from_stock
                    demand -= taken_from_stock
                    lines.append(
                        self._prepare_report_line(taken_from_stock, move_out=out)
                    )
                # Reconcile with the ins.
                r = product.uom_id.rounding
                if not float_is_zero(demand, precision_rounding=r):
                    demand = _reconcile_out_with_ins(
                        lines,
                        out,
                        ins_per_product[out.product_id.id],
                        demand,
                        only_matching_move_dest=True,
                    )
                r = product.uom_id.rounding
                if not float_is_zero(demand, precision_rounding=r):
                    unreconciled_outs.append((demand, out))
            if unreconciled_outs:
                for (demand, out) in unreconciled_outs:
                    demand = _reconcile_out_with_ins(
                        lines,
                        out,
                        ins_per_product[product.id],
                        demand,
                        only_matching_move_dest=False,
                    )
                    r = product.uom_id.rounding
                    if not float_is_zero(demand, precision_rounding=r):
                        # Not reconciled
                        lines.append(
                            self._prepare_report_line(
                                demand, move_out=out, replenishment_filled=False
                            )
                        )
            # Unused remaining stock.
            free_stock = currents.get(product.id, 0)
            r = product.uom_id.rounding
            if not float_is_zero(free_stock, precision_rounding=r):
                lines.append(self._prepare_report_line(free_stock, product=product))
            # In moves not used.
            for in_ in ins_per_product[product.id]:
                r = product.uom_id.rounding
                if float_is_zero(in_["qty"], precision_rounding=r):
                    continue
                lines.append(self._prepare_report_line(in_["qty"], move_in=in_["move"]))
        return lines

    @api.model
    def get_filter_state(self):
        res = {}
        res["warehouses"] = self.env["stock.warehouse"].search_read(
            fields=["id", "name", "code"]
        )
        res["active_warehouse"] = self.env.context.get("warehouse", False)
        if not res["active_warehouse"]:
            company_id = self.env.context.get("allowed_company_ids")[0]
            res["active_warehouse"] = (
                self.env["stock.warehouse"]
                .search([("company_id", "=", company_id)], limit=1)
                .id
            )
        return res
