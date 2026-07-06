# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class RepairOrder(models.Model):
    _inherit = "repair.order"

    bom_id = fields.Many2one(
        comodel_name="mrp.bom",
        string="Bill of Materials",
        domain="['&', ('eligible_in_repairs', '=', True), '|', "
        "('company_id', '=', False), ('company_id', '=', company_id)]",
        check_company=True,
        copy=False,
        help="Bill of materials eligible in repairs used to create the "
        "manufacturing order.",
    )
    production_ids = fields.One2many(
        comodel_name="mrp.production",
        inverse_name="repair_id",
        string="Manufacturing Orders",
        copy=False,
    )
    production_count = fields.Integer(
        string="Manufacturing Orders Count",
        compute="_compute_production_count",
    )
    has_open_production = fields.Boolean(
        string="Has Open Manufacturing Order",
        compute="_compute_has_open_production",
        help="Technical field: True if there is any manufacturing order that "
        "is still open, i.e. not cancelled nor done.",
    )
    has_done_production = fields.Boolean(
        string="Has Done Manufacturing Order",
        compute="_compute_has_done_production",
        help="Technical field: True if there is any manufacturing order in "
        "done state.",
    )

    @api.depends("production_ids")
    def _compute_production_count(self):
        for repair in self:
            repair.production_count = len(repair.production_ids)

    @api.depends("production_ids.state")
    def _compute_has_open_production(self):
        for repair in self:
            repair.has_open_production = any(
                production.state not in ("cancel", "done")
                for production in repair.production_ids
            )

    @api.depends("production_ids.state")
    def _compute_has_done_production(self):
        for repair in self:
            repair.has_done_production = any(
                production.state == "done" for production in repair.production_ids
            )

    def _get_production_picking_type(self):
        self.ensure_one()
        if self.bom_id.picking_type_id:
            return self.bom_id.picking_type_id
        return self.env["stock.picking.type"].search(
            [
                ("code", "=", "mrp_operation"),
                ("warehouse_id.company_id", "=", self.company_id.id),
            ],
            limit=1,
        )

    def _prepare_production_values(self):
        self.ensure_one()
        bom = self.bom_id
        product = bom.product_id or bom.product_tmpl_id.product_variant_id
        picking_type = self._get_production_picking_type()
        location_src = picking_type.default_location_src_id
        location_dest = picking_type.default_location_dest_id
        if not location_src or not location_dest:
            warehouse = self.env["stock.warehouse"].search(
                [("company_id", "=", self.company_id.id)], limit=1
            )
            location_src = location_src or warehouse.lot_stock_id
            location_dest = location_dest or warehouse.lot_stock_id
        values = {
            "repair_id": self.id,
            "bom_id": bom.id,
            "product_id": product.id,
            "product_qty": 1.0,
            "company_id": self.company_id.id,
            "origin": self.name,
        }
        # Set the operation type and locations explicitly so the manufacturing
        # order is created with valid required locations even when other modules
        # alter the precompute of these fields.
        if picking_type:
            values["picking_type_id"] = picking_type.id
        if location_src:
            values["location_src_id"] = location_src.id
        if location_dest:
            values["location_dest_id"] = location_dest.id
        return values

    def action_create_production(self):
        self.ensure_one()
        if not self.bom_id:
            raise UserError(
                _(
                    "You must select a Bill of Materials eligible in repairs "
                    "to create a manufacturing order."
                )
            )
        production = self.env["mrp.production"].create(
            self._prepare_production_values()
        )
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "mrp.mrp_production_action"
        )
        action["views"] = [(False, "form")]
        action["res_id"] = production.id
        action["context"] = {"default_repair_id": self.id}
        return action

    def action_view_productions(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "mrp.mrp_production_action"
        )
        action["domain"] = [("repair_id", "=", self.id)]
        action["context"] = {"default_repair_id": self.id}
        if self.production_count == 1:
            action["views"] = [(False, "form")]
            action["res_id"] = self.production_ids.id
        return action
