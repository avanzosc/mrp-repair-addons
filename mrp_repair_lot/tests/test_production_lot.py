# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestProductionLot(common.TransactionCase):

    def setUp(self):
        super(TestProductionLot, self).setUp()
        self.product1 = self.env.ref('product.product_product_3')
        self.product_uom = self.env.ref('product.product_uom_unit')
        self.stock_location = self.env.ref('stock.stock_location_locations')
        self.lot_model = self.env['stock.production.lot']
        self.repair_model = self.env['mrp.repair']
        self.lot1 = self.lot_model.create(
            {'name': 'LOT1',
             'product_id': self.product1.id})
        self.product2 = self.env.ref('product.product_product_4')

    def test_repair_order_lot(self):
        self.repair1 = self.repair_model.create(
            {'product_id': self.product1.id,
             'lot_id': self.lot1.id,
             'product_uom': self.product_uom.id,
             'location_dest_id': self.stock_location.id,
             })
        self.assertEqual(len(self.lot1.repair_orders), self.lot1.repairs_count)

    def test_respair_order_lot_products(self):
        self.repair2 = self.repair_model.create(
            {'product_id': self.product1.id,
             'lot_id': self.lot1.id,
             'product_uom': self.product_uom.id,
             'location_dest_id': self.stock_location.id,
             })
        self.repair3 = self.repair_model.create(
            {'product_id': self.product2.id,
             'lot_id': self.lot1.id,
             'product_uom': self.product_uom.id,
             'location_dest_id': self.stock_location.id,
             })
        self.assertEqual(len(self.lot1.repair_orders), self.lot1.repairs_count)
