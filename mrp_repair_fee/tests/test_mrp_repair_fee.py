# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestMrpRepairFee(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairFee, self).setUp()
        self.user_model = self.env['res.users']
        self.fee_model = self.env['mrp.repair.fee']
        self.demo_user_id = self.ref('base.user_demo')
        self.employees = self.env['hr.employee'].search(
            [('user_id', '=', self.demo_user_id)])
        self.unit_uom = self.browse_ref('product.product_uom_unit')
        self.location_id = self.ref('stock.stock_location_7')
        fee_vals = {'user_id': self.ref('base.user_root'),
                    'name': 'Fee line test',
                    'product_uom': self.unit_uom.id,
                    'price_unit': 1,
                    'product_uom_qty': 5}
        vals = {'product_id': self.ref('product.product_product_8'),
                'product_uom': self.unit_uom.id,
                'location_id': self.location_id,
                'location_dest_id': self.location_id,
                'fees_lines': [(0, 0, fee_vals)]}
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
