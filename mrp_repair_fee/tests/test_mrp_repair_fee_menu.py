# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestMrpFeeMenu(common.TransactionCase):

    def setUp(self):
        super(TestMrpFeeMenu, self).setUp()
        fee_vals = {'user_id': self.env.ref('base.user_root').id,
                    'name': 'Fee line test',
                    'product_uom': self.env.ref('product.product_uom_unit').id,
                    'price_unit': 1,
                    'product_uom_qty': 5}
        vals = {'product_id': self.env.ref('product.product_product_8').id,
                'product_uom': self.env.ref('product.product_uom_unit').id,
                'location_id': self.env.ref('stock.stock_location_7').id,
                'location_dest_id': self.env.ref('stock.stock_location_7').id,
                'fees_lines': [(0, 0, fee_vals)]}
        self.repair = self.env['mrp.repair'].create(vals)

    def test_mrp_repair_fee(self):
        self.assertEqual(
            len(self.repair.fees_lines_no_to_invoice), 1,
            'Repair without fee to not invoice')
        self.repair.fees_lines_no_to_invoice[:1]._onchange_user_id()
        self.assertEqual(
            self.repair.fees_lines_no_to_invoice[:1].product_id.id,
            self.env.ref('product.product_product_consultant').id,
            'Wrong Product for the administrator user')
