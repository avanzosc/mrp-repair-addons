# Copyright 2024 - Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class RepairLine(models.Model):
    _inherit = "repair.line"

    available_in_location = fields.Float(
        string="Available In Location",
        compute="_compute_available_in_location",
        digits="Product Unit of Measure",
        compute_sudo=False,
    )

    def _compute_available_in_location(self):
        for line in self:
            available_in_location = 0
            if line.product_id and line.location_id:
                available_in_location = line.product_id.with_context(
                    location=line.location_id.id
                ).virtual_available
            line.available_in_location = available_in_location

    def action_repair_line_forecast_report(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "repair_line_forecasted_qty.stock_replenishment_repair_line_action"
        )
        return action

    def action_product_forecast_report(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.stock_replenishment_product_product_action"
        )
        return action
