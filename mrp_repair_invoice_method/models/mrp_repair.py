# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    @api.multi
    @api.onchange('invoice_method')
    def _onchange_invoice_method(self):
        if self.invoice_method != 'none' and not self.partner_invoice_id:
            addr = self.partner_id.address_get(['invoice'])
            self.partner_invoice_id = addr['invoice']
