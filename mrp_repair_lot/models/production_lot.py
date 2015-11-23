# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín <esthermartin@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    repair_orders = fields.One2many(
        comodel_name='mrp.repair', inverse_name='lot_id',
        string='Repair order')

    @api.multi
    @api.depends('repair_orders')
    def _compute_repairs_count(self):
        for repair in self:
            repair.repairs_count = len(repair.repair_orders)

    repairs_count = fields.Integer(compute='_compute_repairs_count',
                                   string='Repair orders')
