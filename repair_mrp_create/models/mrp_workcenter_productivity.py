# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    repair_id = fields.Many2one(
        comodel_name="repair.order",
        string="Repair Order",
        related="workorder_id.repair_id",
        store=True,
        index=True,
    )
