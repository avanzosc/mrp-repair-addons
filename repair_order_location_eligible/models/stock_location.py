# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    eligible_for_repairs = fields.Boolean(string="Eligible for repairs", default=False)
