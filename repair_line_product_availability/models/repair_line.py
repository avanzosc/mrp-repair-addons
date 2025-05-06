# Copyright 2025 - Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class RepairLine(models.Model):
    _inherit = "repair.line"

    def action_view_product_forecast_report(self):
        self.ensure_one()
        result = self.product_id.with_context(
            active_model="product.product",
            active_id=self.product_id.id,
            active_ids=self.product_id.ids,
            default_product_id=self.product_id.id,
        ).action_product_forecast_report()
        return result
