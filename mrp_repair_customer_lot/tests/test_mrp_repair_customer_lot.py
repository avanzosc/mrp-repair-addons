# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestMrpRepairCustomerLot(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairCustomerLot, self).setUp()
        self.data_model = self.env['ir.model.data']
        self.product_model = self.env['product.product']
        self.mrp_repair_model = self.env['mrp.repair']
        self.lot_model = self.env['stock.production.lot']
        self.partner = self.env.ref('base.res_partner_2')
        self.product = self.env.ref('product.product_product_6')
        self.warehouse = self.data_model.get_object('stock', 'warehouse0')
        vals = {'product_id': self.product.id,
                'customer': self.partner.id}
        self.lot = self.lot_model.create(vals)

    def test_mrp_repair_onchange_lot(self):
        vals = {'product_id': self.product.id,
                'location_id': self.warehouse.lot_stock_id.id,
                'location_dest_id': self.warehouse.lot_stock_id.id,
                'product_uom': self.product.uom_id.id,
                'lot_id': self.lot.id}
        mrp_repair = self.mrp_repair_model.create(vals)
        mrp_repair.onchange_lot_id()
        self.assertEqual(
            mrp_repair.partner_id.id, self.partner.id,
            'Repair order created without customer')

    def test_customer_num_lots(self):
        self.assertEqual(
            self.partner.num_lots, 1, 'Customer does not have assigned lots')
