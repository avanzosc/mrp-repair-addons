# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín <esthermartin@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestRepairExpense(common.TransactionCase):

    def setUp(self):
        super(TestRepairExpense, self).setUp()
        self.product1 = self.env.ref('product.product_product_3')
        self.product_uom = self.env.ref('product.product_uom_unit')
        self.stock_location = self.env.ref('stock.stock_location_locations')
        self.repair_model = self.env['mrp.repair']
        self.repair1 = self.repair_model.create(
            {'product_id': self.product1.id,
             'product_uom': self.product_uom.id,
             'product_qty': 1.0,
             'location_id': self.stock_location.id,
             'name': 'Repair order 1',
             'location_dest_id': self.stock_location.id,
             })

    def test_repair_order_expenses(self):
        self.expenses = self.env.ref('hr_expense.sep_expenses')
        self.expenses.repair_order = self.repair1.id
        self.assertEqual(len(self.repair1.expenses),
                         self.repair1.expense_count)
