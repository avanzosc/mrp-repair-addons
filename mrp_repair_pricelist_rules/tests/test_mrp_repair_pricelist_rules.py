# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestMrpRepairPricelistRules(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairPricelistRules, self).setUp()
        self.mrp_repair_model = self.env['mrp.repair']
        self.pricelist = self.env.ref('product.list0')
        self.pricelist_item = self.env.ref('product.item0')
        self.pricelist_item.discount = 25
        # Product: Webcam -- Standard Price: 38.0
        self.op_product = self.env.ref('product.product_product_34')
        self.op_product.cost_method = 'average'
        self.op_product.standard_price = 30
        default_location = self.mrp_repair_model._default_stock_location()
        op_val = {
            'product_id': self.op_product.id,
            'product_uom_qty': 3,
            'name': self.op_product.name,
            'item_id': self.pricelist_item.id,
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
            'name': self.op2_product.name,
            'item_id': self.pricelist_item.id,
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
            'product_uom': self.repair_product.uom_id.id,
            'product_id': self.repair_product.id,
            'partner_id': self.env.ref('base.res_partner_8').id,
            'pricelist_id': self.pricelist.id,
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
        op_line.onchange_item_id()
        op2_line.onchange_item_id()
        op_subtotal = round((op_line.product_uom_qty * op_line.price_unit *
                             (1 - op_line.discount/100)), 2)
        op2_subtotal = round((op2_line.product_uom_qty * op2_line.price_unit *
                              (1 - op2_line.discount/100)), 2)
        self.assertEqual(op_line.price_subtotal, op_subtotal,
                         "Incorrect subtotal")
        self.assertEqual(op2_line.price_subtotal, op2_subtotal,
                         "Incorrect subtotal.")

    def test_mrp_repair_line_discount(self):
        op_line = self.mrp_repair.operations.filtered(
            lambda x: x.product_id.id == self.op_product.id)
        op2_line = self.mrp_repair.operations.filtered(
            lambda x: x.product_id.id == self.op2_product.id)
        op_line.onchange_item_id()
        op2_line.onchange_item_id()
        self.assertEqual(op_line.discount, 25,
                         "Incorrect discount.")
        self.assertEqual(op2_line.discount, 25,
                         "Incorrect discount.")

    def test_mrp_repair_invoice(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        self.mrp_repair.action_invoice_create()
        for line in self.mrp_repair.operations:
            self.assertEqual = (line.invoice_line_id.discount, line.discount,
                                "Incorrect invoice line qty.")

    def test_mrp_repair_line_product_change(self):
        repair_line_obj = self.env['mrp.repair.line']
        res = repair_line_obj.product_id_change(
            self.mrp_repair.pricelist_id.id, self.op2_product.id,
            uom=self.op2_product.uom_id.id, product_uom_qty=0,
            partner_id=self.mrp_repair.partner_id.id)
        self.assertEqual = (res['value']['item_id'], self.pricelist_item.id,
                            "Product item changed in onchange.")
        repair_fee_obj = self.env['mrp.repair.fee']
        res = repair_fee_obj.product_id_change(
            self.mrp_repair.pricelist_id.id, self.op2_product.id,
            uom=self.op2_product.uom_id.id, product_uom_qty=0,
            partner_id=self.mrp_repair.partner_id.id)
        self.assertEqual = (res['value']['item_id'], self.pricelist_item.id,
                            "Product item changed in onchange.")
