# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín <esthermartin@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    expenses = fields.One2many(string='Expenses',
                               comodel_name='hr.expense.expense',
                               inverse_name='repair_order')
    expense_lines = fields.One2many(string='Expenses',
                                    comodel_name='hr.expense.line',
                                    inverse_name='repairs')

    @api.multi
    @api.depends('expenses')
    def _hr_expense_count(self):
        for expense in self:
            expense.expense_count = len(expense.expenses)

    expense_count = fields.Integer(compute='_hr_expense_count',
                                   string='Expenses')
