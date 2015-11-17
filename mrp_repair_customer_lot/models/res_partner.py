# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _count_num_lots(self):
        lot_obj = self.env['stock.production.lot']
        for partner in self:
            cond = [('customer', '=', partner.id)]
            lots = lot_obj.search(cond)
            partner.num_lots = len(lots)

    num_lots = fields.Integer(compute='_count_num_lots', string='Lots')
