# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    @api.multi
    @api.depends('analytic_account', 'analytic_account.line_ids',
                 'analytic_account.line_ids.amount')
    def _compute_repair_real_lines(self):
        for record in self:
            lines = record.analytic_account.line_ids.filtered(
                lambda x: x.amount)
            record.repair_real_lines = lines

    @api.multi
    @api.depends('analytic_account', 'analytic_account.line_ids',
                 'analytic_account.line_ids.repair_estim_amount')
    def _compute_repair_estim_lines(self):
        for record in self:
            lines = record.analytic_account.line_ids.filtered(
                lambda x: x.repair_estim_amount)
            record.repair_estim_lines = lines

    repair_estim_lines = fields.Many2many(
        comodel_name="account.analytic.line", relation="repair_estimated_cost",
        column1="repair_id", column2="analytic_line_id", copy=False,
        string="Estimated costs", compute='_compute_repair_estim_lines')
    repair_real_lines = fields.Many2many(
        comodel_name="account.analytic.line", relation="repair_real_cost",
        column1="repair_id", column2="analytic_line_id", string="Real costs",
        copy=False, compute='_compute_repair_real_lines')

    @api.multi
    def action_confirm(self):
        self.with_context(load_estimated=True).create_repair_cost()
        return super(MrpRepair, self).action_confirm()

    def _catch_repair_line_information_for_analytic(self, line):
        analytic_line_obj = self.env['account.analytic.line']
        ctx = self.env.context or {}
        line_cond = [('account_id', '=', self.analytic_account.id),
                     ('product_id', '=', line.product_id.id),
                     ('is_repair_cost', '!=', True)]
        if analytic_line_obj.search(line_cond):
            return False
        res = super(MrpRepair,
                    self)._catch_repair_line_information_for_analytic(line)
        if res and ctx.get('load_estimated', False):
            res['repair_estim_amount'] = res.get('amount', 0)
            res['amount'] = 0
        return res

    @api.multi
    def create_repair_cost(self):
        analytic_line_obj = self.env['account.analytic.line']
        super(MrpRepair, self).create_repair_cost()
        if not self.env.context.get('load_estimated', False):
            return
        for line in self.mapped('fees_lines').filtered(lambda x:
                                                       not x.load_cost):
            vals = self._catch_repair_line_information_for_analytic(line)
            if vals:
                analytic_line_obj.create(vals)
        for line in self.mapped('operations').filtered(
                lambda x: not x.load_cost and x.type == 'add'):
            vals = self._catch_repair_line_information_for_analytic(line)
            if vals:
                analytic_line_obj.create(vals)
