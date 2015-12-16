# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    @api.model
    def create(self, values):
        if 'partner_id' in values:
            vals = {'name': values.get('name'),
                    'partner_id': values.get('partner_id'),
                    'type': 'normal'}
            account = self.env['account.analytic.default'].account_get(
                partner_id=values.get('partner_id'),
                company_id=self.env.user.company_id.id)
            if account:
                vals['parent_id'] = account.analytic_id.id
            analytic = self.env['account.analytic.account'].create(vals)
            values['analytic_account'] = analytic.id
        repair = super(MrpRepair, self).create(values)
        return repair
