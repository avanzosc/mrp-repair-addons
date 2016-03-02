# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestMrpRepairEstimatedQty(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairEstimatedQty, self).setUp()
        self.mrp_repair_model = self.env['mrp.repair']
        self.analytic_account_model = self.env['account.analytic.account']
        self.analytic_line_model = self.env['account.analytic.line']
        analytic_vals = {
            'name': 'Repair Cost Account',
            'type': 'normal',
            }
        self.analytic_id = self.analytic_account_model.create(analytic_vals)
        # Product: Webcam -- Standard Price: 38.0
        self.op_product = self.env.ref('product.product_product_34')
        self.op_product.cost_method = 'average'
        self.op_product.standard_price = 30
        default_location = self.mrp_repair_model._default_stock_location()
        op_val = {
            'product_id': self.op_product.id,
            'product_uom_qty': 3,
            'expected_qty': 2,
            'name': self.op_product.name,
            'product_uom': self.op_product.uom_id.id,
            'type': 'add',
            'location_id': default_location,
            'location_dest_id': self.op_product.property_stock_production.id,
            'price_unit': 1.5,
            'to_invoice': True,
            'load_cost': True,
            }
        self.op_amount = (-1 * self.op_product.standard_price * 2)
        # Product: On Site Monitoring -- Standard Price: 20.5
        self.op2_product = self.env.ref('product.product_product_1')
        op_val2 = {
            'product_id': self.op2_product.id,
            'product_uom_qty': 3,
            'expected_qty': 0,
            'name': self.op2_product.name,
            'product_uom': self.op2_product.uom_id.id,
            'type': 'add',
            'location_id': default_location,
            'location_dest_id': self.op2_product.property_stock_production.id,
            'price_unit': 2,
            'to_invoice': True,
            'load_cost': True,
            }
        self.op2_amount = (-1 * self.op2_product.standard_price * 3)
        self.repair_product = self.env.ref('product.product_product_27')
        repair_vals = {
            'analytic_account': self.analytic_id.id,
            'product_uom': self.repair_product.uom_id.id,
            'product_id': self.repair_product.id,
            'partner_id': self.env.ref('base.res_partner_8').id,
            'location_id': default_location,
            'location_dest_id': default_location,
            'operations': [(0, 0, op_val), (0, 0, op_val2)],
            'invoice_method': 'after_repair',
            'partner_invoice_id': self.env.ref('base.res_partner_8').id
            }
        self.mrp_repair = self.mrp_repair_model.create(repair_vals)

    def test_mrp_repair_line_subtotal(self):
        op_line = self.mrp_repair.operations.filtered(
            lambda x: x.product_id.id == self.op_product.id)
        op2_line = self.mrp_repair.operations.filtered(
            lambda x: x.product_id.id == self.op2_product.id)
        self.assertEqual(op_line.price_subtotal, 3,
                         "Incorrect subtotal with expected amount.")
        self.assertEqual(op2_line.price_subtotal, 0,
                         "Incorrect subtotal with no expected amount.")

    def test_mrp_repair_line_cost_subtotal(self):
        op_line = self.mrp_repair.operations.filtered(
            lambda x: x.product_id.id == self.op_product.id)
        op2_line = self.mrp_repair.operations.filtered(
            lambda x: x.product_id.id == self.op2_product.id)
        self.assertEqual(op_line.cost_subtotal,
                         (self.op_product.standard_price * 2),
                         "Incorrect cost subtotal with expected amount.")
        self.assertEqual(op2_line.cost_subtotal,
                         (self.op2_product.standard_price * 0),
                         "Incorrect cost subtotal with no expected amount.")

    def test_mrp_repair_create_cost_with_estimated_qty_confirm(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        ope_line = self.analytic_line_model.search(
            [('account_id', '=', self.analytic_id.id),
             ('product_id', '=', self.op_product.id),
             ('unit_amount', '=', 2),
             ('is_repair_cost', '=', True),
             ('amount', '=', 0),
             ('repair_estim_amount', '=', self.op_amount)])
        fee_line = self.analytic_line_model.search(
            [('account_id', '=', self.analytic_id.id),
             ('product_id', '=', self.op2_product.id),
             ('unit_amount', '=', 3),
             ('is_repair_cost', '=', True),
             ('amount', '=', 0),
             ('repair_estim_amount', '=', self.op2_amount)])
        self.assertNotEqual(len(ope_line), 0,
                            "Operation with expected qty line not found.")
        self.assertEqual(len(fee_line), 0,
                         "Operation with not expected qty line not found.")

    def test_mrp_repair_create_cost_with_zero_uom_qty_confirm(self):
        op_line = self.mrp_repair.operations.filtered(
            lambda x: x.product_id.id == self.op_product.id)
        op_line.product_uom_qty = 0
        self.mrp_repair.signal_workflow('repair_confirm')
        ope_line = self.analytic_line_model.search(
            [('account_id', '=', self.analytic_id.id),
             ('product_id', '=', self.op_product.id),
             ('unit_amount', '=', 2),
             ('is_repair_cost', '=', True),
             ('amount', '=', 0),
             ('repair_estim_amount', '=', self.op_amount)])
        fee_line = self.analytic_line_model.search(
            [('account_id', '=', self.analytic_id.id),
             ('product_id', '=', self.op2_product.id),
             ('unit_amount', '=', 3),
             ('is_repair_cost', '=', True),
             ('amount', '=', 0),
             ('repair_estim_amount', '=', self.op2_amount)])
        self.assertNotEqual(len(ope_line), 0,
                            "Operation with expected qty line not found.")
        self.assertEqual(len(fee_line), 0,
                         "Operation with not expected qty line not found.")

    def test_mrp_repair_invoice_with_expected_qty(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        self.mrp_repair.action_invoice_create()
        for line in self.mrp_repair.operations:
            qty = line.product_uom_qty
            if line.expected_qty:
                qty = line.expected_qty
            self.assertEqual = (line.invoice_line_id.quantity, qty,
                                "Incorrect invoice line qty.")

    def test_mrp_repair_line_product_change(self):
        repair_line_obj = self.env['mrp.repair.line']
        res = repair_line_obj.product_id_change(
            self.mrp_repair.pricelist_id.id, self.op2_product.id,
            uom=self.op2_product.uom_id.id, product_uom_qty=0,
            partner_id=self.mrp_repair.partner_id.id)
        self.assertEqual = (res['value']['product_uom_qty'], 0,
                            "Product uom qty changed in onchange.")
