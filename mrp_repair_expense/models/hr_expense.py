# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín <esthermartin@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class HrExpenseExpense(models.Model):
    _inherit = 'hr.expense.expense'

    repair_order = fields.Many2one(string='Repair order',
                                   comodel_name='mrp.repair')
    repair_analytic_account = fields.Many2one(
        related='repair_order.analytic_account')

    @api.multi
    @api.onchange('repair_order')
    def onchange_repair_order(self):
        for line in self.line_ids:
            line.analytic_account = self.repair_order.analytic_account
            line.repairs = self.repair_order


class HrExpenseLine(models.Model):
    _inherit = 'hr.expense.line'

    repairs = fields.Many2one(string='Repair order', comodel_name='mrp.repair')
