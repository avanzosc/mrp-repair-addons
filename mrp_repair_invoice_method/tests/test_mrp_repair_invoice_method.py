# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín- AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestMrpRepairInvoiceMethod(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairInvoiceMethod, self).setUp()
        self.mrp_repair_model = self.env['mrp.repair']
        self.mrp_repair = self.mrp_repair_model.create({
            'name': 'RMA012',
            'product_id': self.ref('product.product_product_6'),
            'partner_id': self.ref('base.res_partner_2'),
            'product_uom': self.ref('product.product_uom_unit'),
            'location_dest_id': self.ref('stock.stock_location_14'),
            })

    def test_mrp_repair_onchange_invoice_method(self):
        self.mrp_repair.invoice_method = 'b4repair'
        self.mrp_repair._onchange_invoice_method()
        self.assertEqual(
            self.mrp_repair.partner_invoice_id.id,
            self.mrp_repair.partner_id.id,
            'The partner invoice and partner are not the same')
