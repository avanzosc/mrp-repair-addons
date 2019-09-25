# -*- coding: utf-8 -*-
# Copyright 2018 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    is_in_warranty = fields.Boolean(string='In warranty')

    @api.onchange('is_in_warranty')
    def onchange_warranty(self):
        for repair in self.filtered('is_in_warranty'):
            repair.invoice_method = 'none'
