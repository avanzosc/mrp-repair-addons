# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    repair_id = fields.Many2one(
        comodel_name="repair.order",
        string="Repair Order",
        related="production_id.repair_id",
        store=True,
        index=True,
    )
