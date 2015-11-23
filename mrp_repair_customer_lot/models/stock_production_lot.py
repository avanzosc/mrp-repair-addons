# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    customer = fields.Many2one(comodel_name='res.partner', string='Customer')
