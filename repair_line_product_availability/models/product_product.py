# Copyright 2024 - Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_product_forecast_report(self):
        self.ensure_one()
        result = super(ProductProduct, self).action_product_forecast_report()
        return result
