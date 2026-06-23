# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    eligible_in_repairs = fields.Boolean(
        string="Eligible in repairs",
        help="If checked, this bill of materials can be selected in repair "
        "orders to create their manufacturing order.",
    )
