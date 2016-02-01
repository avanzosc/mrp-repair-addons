# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestMrpRepairFee(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairFee, self).setUp()
        self.user_model = self.env['res.users']
        self.fee_model = self.env['mrp.repair.fee']
        self.lot_model = self.env['stock.production.lot']
        self.location_model = self.env['stock.location']
        self.quant_model = self.env['stock.quant']
        self.demo_user_id = self.ref('base.user_demo')
        self.employees = self.env['hr.employee'].search(
            [('user_id', '=', self.demo_user_id)])
        self.unit_uom = self.browse_ref('product.product_uom_unit')
        self.location_id = self.ref('stock.stock_location_7')
        internal_location = self.location_model.search([('usage', '=',
                                                         'internal')], limit=1)
        self.repair_line_product = self.env.ref('product.product_product_10')
        self.repair_line_product.cost_method = 'real'
        self.lot_id = self.lot_model.create(
            {'product_id': self.repair_line_product.id,
             'name': 'LOT-TEST'})
        self.quant_model.create(
            {'product_id': self.repair_line_product.id,
             'lot_id': self.lot_id.id,
             'cost': 11,
             'location_id': internal_location.id,
             'qty': 5})
        repair_line_vals = {
            'user_id': self.ref('base.user_root'),
            'name': 'Repair line',
            'product_uom': self.unit_uom.id,
            'product_id': self.repair_line_product.id,
            'lot_id': self.lot_id.id,
            'price_unit': 1,
            'product_uom_qty': 5,
            'location_id': internal_location.id,
            'location_dest_id': internal_location.id,
            'type': 'add'}
        fee_vals = {'user_id': self.ref('base.user_root'),
                    'name': 'Fee line test',
                    'product_uom': self.unit_uom.id,
                    'price_unit': 1,
                    'product_uom_qty': 5}
        vals = {'product_id': self.ref('product.product_product_8'),
                'product_uom': self.unit_uom.id,
                'location_id': self.location_id,
                'location_dest_id': self.location_id,
                'fees_lines': [(0, 0, fee_vals)],
                'operations': [(0, 0, repair_line_vals)]}
        self.repair = self.env['mrp.repair'].with_context(
            to_invoice=False).create(vals)

    def test_mrp_repair_fee(self):
        self.assertEqual(
            len(self.repair.fees_lines_no_to_invoice), 1,
            'Repair without fee to not invoice')
        self.repair.fees_lines_no_to_invoice[:1]._onchange_user_id()
        self.assertEqual(
            self.repair.fees_lines_no_to_invoice[:1].product_id.id,
            self.ref('product.product_product_consultant'),
            'Wrong Product for the administrator user')

    def test_mrp_repair_fee_without_employee(self):
        self.employees.write({'user_id': False})
        fee_vals = {'user_id': self.demo_user_id,
                    'repair_id': self.repair.id,
                    'to_invoice': True,
                    'name': 'Fee line test',
                    'product_uom': self.unit_uom.id,
                    'price_unit': 1,
                    'product_uom_qty': 5}
        fee = self.fee_model.create(fee_vals)
        res = fee._onchange_user_id()
        self.assertTrue(
            'warning' in res, 'Onchange warning must have been launched')
        self.assertEqual(
            len(fee.product_id), 0, 'Line should not have product')

    def test_mrp_repair_fee_without_employee_product(self):
        self.employees.write({'product_id': False})
        fee_vals = {'user_id': self.demo_user_id,
                    'repair_id': self.repair.id,
                    'to_invoice': True,
                    'name': 'Fee line test',
                    'product_uom': self.unit_uom.id,
                    'price_unit': 1,
                    'product_uom_qty': 5}
        fee = self.fee_model.create(fee_vals)
        res = fee._onchange_user_id()
        self.assertTrue(
            'warning' in res, 'Onchange warning must have been launched')
        self.assertEqual(
            len(fee.product_id), 0, 'Line should not have product')
        res = fee.onchange_repair_id()
        self.assertTrue(
            'warning' in res, 'Onchange 2 warning must have been launched')
        res = fee.product_id_change(False, fee.product_id.id)
        self.assertTrue(
            'warning' in res, 'Onchange 3 warning must have been launched')

    def test_mrp_repair_fee_wizard(self):
        wiz = self.env['wiz.mrp.repair.fee'].create(
            {'imputation_date': '2015-12-16'})
        res = wiz.show_mrp_repair_fee()
        context = res.get('context')
        self.assertIn(
            'default_imputation_date', context,
            'Default imputation date not found in context')
        self.assertEqual(
            '2015-12-16', context.get('default_imputation_date'),
            'Default imputation date not equal 2015-12-16')
        self.assertIn(
            'default_to_invoice', context,
            'Default to invoice not found in context')

    def test_mrp_repair_line_cost(self):
        for operation in self.repair.operations:
            cost = 0
            if operation.product_id.cost_method == 'real' and operation.lot_id:
                quants = operation.lot_id.quant_ids.filtered(
                    lambda x: x.location_id.usage == 'internal')
                if quants:
                    cost = quants[:1].cost
            else:
                cost = operation.product_id.standard_price
            self.assertEqual(operation.standard_price, cost,
                             "Operation line cost is not correct.")
