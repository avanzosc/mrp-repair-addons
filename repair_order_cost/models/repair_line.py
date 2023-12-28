# Copyright 2023 - Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairLine(models.Model):
    _inherit = "repair.line"

    material_cost = fields.Float(
        string="Material cost", digits="Product Price"
    )

    @api.onchange("repair_id", "product_id", "product_uom_qty")
    def onchange_product_id(self):
        result = super(RepairLine, self).onchange_product_id()
        material_cost = 0
        if self.type and self.type == "add" and self.product_id:
            material_cost = (
                self.product_uom_qty * self.product_id.standard_price)
        self.material_cost = material_cost
        return result
