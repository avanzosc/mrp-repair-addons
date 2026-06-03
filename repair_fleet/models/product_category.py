# Copyright 2025 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    repairable = fields.Boolean(
        string='Repairable',
        default=False,
    )
