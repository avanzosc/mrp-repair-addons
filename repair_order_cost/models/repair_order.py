# Copyright 2023 - Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    material_cost = fields.Float(
        string="Material cost",
        digits="Product Price",
        compute="_compute_repair_costs",
        store=True,
        copy=False,
        readonly=False,
    )
    operations_cost = fields.Float(
        string="Operations cost",
        digits="Product Price",
        compute="_compute_repair_costs",
        store=True,
        copy=False,
        readonly=False,
    )
    total_repair_cost = fields.Float(
        string="Total repair cost",
        digits="Product Price",
        compute="_compute_total_repair_costs",
        store=True,
        copy=False,
        readonly=False,
    )

    @api.depends(
        "move_ids",
        "move_ids.material_cost",
        "repair_service_ids",
        "repair_service_ids.operations_cost",
    )
    def _compute_repair_costs(self):
        for repair in self:
            material_cost = 0
            operations_cost = 0
            if repair.move_ids:
                material_cost = sum(repair.move_ids.mapped("material_cost"))
            if repair.repair_service_ids:
                operations_cost = sum(
                    repair.repair_service_ids.mapped("operations_cost")
                )
            repair.material_cost = material_cost
            repair.operations_cost = operations_cost

    @api.depends("material_cost", "operations_cost")
    def _compute_total_repair_costs(self):
        for repair in self:
            repair.total_repair_cost = repair.material_cost + repair.operations_cost
