# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, models


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    @api.multi
    @api.onchange('lot_id')
    def onchange_lot_id(self):
        self.ensure_one()
        if self.lot_id:
            self.partner_id = self.lot_id.customer.id
