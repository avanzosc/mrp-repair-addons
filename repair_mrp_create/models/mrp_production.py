# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    repair_id = fields.Many2one(
        comodel_name="repair.order",
        string="Repair Order",
        check_company=True,
        copy=False,
        index=True,
        help="Repair order that generated this manufacturing order.",
    )
