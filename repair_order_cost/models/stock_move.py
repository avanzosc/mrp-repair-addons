# Copyright 2023 - Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    material_cost = fields.Float(
        string="Material cost",
        digits="Product Price",
        compute="_compute_material_cost",
        store=True,
        copy=False,
    )

    @api.depends(
        "repair_id", "move_line_ids", "move_line_ids.cost", "move_line_ids.state"
    )
    def _compute_material_cost(self):
        for move in self:
            material_cost = 0
            if move.repair_id:
                move.material_cost = sum(
                    move.move_line_ids.filtered(lambda x: x.state == "done").mapped(
                        "cost"
                    )
                )
            move.material_cost = material_cost
