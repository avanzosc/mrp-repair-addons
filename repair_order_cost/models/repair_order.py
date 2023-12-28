# Copyright 2023 - Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    material_cost = fields.Float(
        string="Material cost", digits="Product Price",
        compute="_compute_repair_costs", store=True, copy=False
    )
    operations_cost = fields.Float(
        string="Operations cost", digits="Product Price",
        compute="_compute_repair_costs", store=True, copy=False
    )
    total_repair_cost = fields.Float(
        string="Total repair cost", digits="Product Price",
        compute="_compute_repair_costs", store=True, copy=False
    )

    @api.depends("operations", "operations.material_cost",
                 "fees_lines", "fees_lines.operations_cost")
    def _compute_repair_costs(self):
        for repair in self:
            material_cost = 0
            operations_cost = 0
            if repair.operations:
                material_cost = sum(
                    repair.operations.mapped("material_cost"))
            if repair.fees_lines:
                operations_cost = sum(
                    repair.fees_lines.mapped("operations_cost"))
            repair.material_cost = material_cost
            repair.operations_cost = operations_cost
            repair.total_repair_cost = material_cost + operations_cost
