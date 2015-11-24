# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    expenses = fields.One2many(
        string='Expenses', comodel_name='hr.expense.expense',
        inverse_name='repair_id')
    expense_lines = fields.One2many(
        string='Expense Lines', comodel_name='hr.expense.line',
        inverse_name='repair_id')
    expense_amount = fields.Float(
        compute='_compute_expense_amount', string='Expense Amount')

    @api.multi
    @api.depends('expenses')
    def _compute_expense_amount(self):
        for repair in self:
            repair.expense_amount = sum(repair.mapped('expenses.amount'))
