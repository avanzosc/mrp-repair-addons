# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    repair_eligible = fields.Boolean(
        string='Eligible in Repairs',
        default=False)
