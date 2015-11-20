# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields
from openerp.addons import decimal_precision as dp


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    repair_estim_amount = fields.Float(string='Repair Estim. Amount',
                                       digits=dp.get_precision('Account'))
