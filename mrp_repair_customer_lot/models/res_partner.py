# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_num_lots(self):
        lot_obj = self.env['stock.production.lot']
        for partner in self:
            partner.num_lots = len(
                lot_obj.search([('customer', '=', partner.id)]))

    num_lots = fields.Integer(compute='_compute_num_lots', string='Lots')
