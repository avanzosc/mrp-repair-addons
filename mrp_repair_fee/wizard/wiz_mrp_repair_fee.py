# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _


class WizMrpRepairFee(models.TransientModel):
    _name = 'wiz.mrp.repair.fee'

    imputation_date = fields.Date(string='Imputation Date', required=True)

    @api.multi
    def show_mrp_repair_fee(self):
        self.ensure_one()
        return {'name': _('MRP Repair Fee'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                "view_mode": 'tree,form',
                'res_model': 'mrp.repair.fee',
                'domain': [('imputation_date', '=', self.imputation_date)],
                'context': {'default_imputation_date': self.imputation_date,
                            'default_to_invoice': False}}
