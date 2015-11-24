# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestRepairExpense(common.TransactionCase):

    def setUp(self):
        super(TestRepairExpense, self).setUp()
        self.product1 = self.env.ref('product.product_product_3')
        self.stock_location = self.env.ref('stock.stock_location_locations')
        self.repair_model = self.env['mrp.repair']
        self.repair1 = self.repair_model.create({
            'product_id': self.product1.id,
            'product_uom': self.product1.uom_id.id,
            'product_qty': 1.0,
            'location_id': self.stock_location.id,
            'name': 'Repair order 1',
            'location_dest_id': self.stock_location.id,
        })

    def test_repair_order_expenses(self):
        expense = self.env.ref('hr_expense.sep_expenses')
        expense.repair_id = self.repair1
        expense.onchange_repair_id()
        self.assertEqual(
            len(self.repair1.expenses), self.repair1.expense_count,
            'Computed field is failing')
        for line in expense.line_ids:
            self.assertEqual(
                self.repair1, line.repair_id,
                'Error assigning repair order to lines')
            self.assertEqual(
                self.repair1.analytic_account, line.analytic_account,
                'Error assigning repair order to lines')
