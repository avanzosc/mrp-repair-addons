# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        if "from_repair_order" not in self.env.context:
            return super().create(vals_list)
        my_invoice_line_ids = []
        repairs_treated = self.env["repair.order"]
        fee_pending = True
        for vals in vals_list:
            lines_vals = vals.get("invoice_line_ids")
            fee_pending = True
            line_pending = True
            section_pending = True
            for line_vals in lines_vals:
                if "repair_line_ids" in line_vals[2]:
                    repair_line = self.env["repair.line"].browse(
                        line_vals[2].get("repair_line_ids")[0][1]
                    )
                    if repair_line.repair_id not in repairs_treated or line_pending:
                        if repair_line.repair_id not in repairs_treated:
                            section_pending = True
                            fee_pending = True
                        repairs_treated += repair_line.repair_id
                        my_invoice_line_ids = self._prepare_repair_info_section(
                            repair_line.repair_id,
                            my_invoice_line_ids,
                            section_pending,
                            False,
                        )
                        line_pending = False
                        section_pending = False
                elif "repair_fee_ids" in line_vals[2]:
                    repair_fee = self.env["repair.fee"].browse(
                        line_vals[2].get("repair_fee_ids")[0][1]
                    )
                    if repair_fee.repair_id not in repairs_treated or fee_pending:
                        if repair_fee.repair_id not in repairs_treated:
                            section_pending = True
                            line_pending = True
                        repairs_treated += repair_fee.repair_id
                        my_invoice_line_ids = self._prepare_repair_info_section(
                            repair_fee.repair_id,
                            my_invoice_line_ids,
                            section_pending,
                            True,
                        )
                        fee_pending = False
                        section_pending = False
                my_invoice_line_ids.append(line_vals)
            vals["invoice_line_ids"] = my_invoice_line_ids
        return super().create(vals_list)

    def _prepare_repair_info_section(
        self, repair, line_ids, section_pending, is_operation
    ):
        if section_pending:
            vals = self._prepare_values_for_repair(repair)
            line_ids.append((0, 0, vals))
        my_name = _("OPERATIONS") if is_operation else _("PARTS")
        my_name = _("{} - {}").format(my_name, repair.name)
        vals = {
            "name": my_name,
            "display_type": "line_section",
        }
        line_ids.append((0, 0, vals))
        return line_ids

    def _prepare_values_for_repair(self, repair):
        repair_name = self._get_repair_name_for_values(repair)
        vals = {
            "name": repair_name,
            "display_type": "line_section",
        }
        return vals

    def _get_repair_name_for_values(self, repair):
        repair_name = _(
            "Repair: %(repair)s, VAT: %(vat)s, Product to repair: " "%(product)s"
        ) % {
            "repair": repair.name,
            "vat": repair.partner_id.vat or "",
            "product": repair.product_id.name,
        }
        if repair.lot_id:
            repair_name = _("%(repair_name)s, Lot: %(lot)s") % {
                "repair_name": repair_name,
                "lot": repair.lot_id.name,
            }
        return repair_name
