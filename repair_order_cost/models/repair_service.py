# Copyright 2023 - Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairService(models.Model):
    _inherit = "repair.service"

    operations_cost = fields.Float(string="Operations cost", digits="Product Price")

    @api.onchange("repair_id", "product_id", "product_uom_qty")
    def onchange_product_id(self):
        operations_cost = 0
        if self.product_id:
            operations_cost = self.product_uom_qty * self.product_id.standard_price
        self.operations_cost = operations_cost
