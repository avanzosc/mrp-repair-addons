# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestMrpRepairPartnerLot(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairPartnerLot, self).setUp()
        self.supplierinfo = self.env['product.supplierinfo']. search(
            [], limit=1)
        self.supplierinfo.write(
            {'product_code': 'a1a1a1',
             'product_name': 'AAAAAA'})

    def test_mrp_repair_partner_lot(self):
        res = self.supplierinfo.name_get()
        self.assertEqual(
            str(res),
            "[({}, u'{}')]".format(
                self.supplierinfo.id, self.supplierinfo.name.name))
        res = self.supplierinfo.with_context(
            show_customer_product_code=True).name_get()
        self.assertEqual(
            str(res),
            "[({}, u'[{}] {}')]".format(
                self.supplierinfo.id, self.supplierinfo.product_code,
                self.supplierinfo.product_name))
