# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    analytic_account = fields.Many2one(copy=False)

    @api.multi
    def _create_repair_analytic_account(self):
        for record in self:
            if record.partner_id and not record.analytic_account:
                vals = {
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'type': 'normal',
                }
                account = self.env['account.analytic.default'].account_get(
                    partner_id=record.partner_id.id,
                    company_id=self.env.user.company_id.id)
                if account:
                    vals['parent_id'] = account.analytic_id.id
                analytic = self.env['account.analytic.account'].create(vals)
                record.analytic_account = analytic

    @api.model
    def create(self, values):
        repair = super(MrpRepair, self).create(values)
        repair._create_repair_analytic_account()
        return repair

    @api.multi
    def write(self, values):
        res = super(MrpRepair, self).write(values)
        self._create_repair_analytic_account()
        return res
