# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestMrpRepairPartnerLot(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairPartnerLot, self).setUp()
        self.supplierinfo_model = self.env['product.supplierinfo']
        self.supplier = self.env.ref('base.partner_root')
        self.product = self.env['product.template'].create({
            'name': 'Product',
            'default_code': 'CODE',
        })
        self.supplierinfo = self.supplierinfo_model.create({
            'name': self.supplier.id,
            'product_tmpl_id': self.product.id,
            'product_code': 'SUP CODE',
            'product_name': 'Product Name',
        })

    def test_mrp_repair_partner_lot(self):
        suppinfo = self.supplierinfo_model.name_search('CODE')
        self.assertEqual(self.supplierinfo.name_get(), suppinfo)
        self.assertEqual(
            self.supplierinfo.display_name, self.supplierinfo.name.name)
        self.assertEqual(
            self.supplierinfo.with_context(
                show_customer_product_code=True).display_name,
            '[{}] {}'.format(self.supplierinfo.product_code,
                             self.supplierinfo.product_name))
        self.supplierinfo.write({
            'product_code': '',
            'product_name': 'Product Name',
        })
        self.supplierinfo.invalidate_cache()
        self.assertEqual(
            self.supplierinfo.with_context(
                show_customer_product_code=True).display_name,
            '[{}] {}'.format(self.supplierinfo.product_tmpl_id.default_code,
                             self.supplierinfo.product_name))
        self.supplierinfo.write({
            'product_code': 'SUP CODE',
            'product_name': '',
        })
        self.supplierinfo.invalidate_cache()
        self.assertEqual(
            self.supplierinfo.with_context(
                show_customer_product_code=True).display_name,
            '[{}] {}'.format(self.supplierinfo.product_code,
                             self.supplierinfo.product_tmpl_id.name))
        self.supplierinfo.write({
            'product_code': '',
            'product_name': '',
        })
        self.supplierinfo.invalidate_cache()
        self.assertEqual(
            self.supplierinfo.with_context(
                show_customer_product_code=True).display_name,
            '[{}] {}'.format(self.supplierinfo.product_tmpl_id.default_code,
                             self.supplierinfo.product_tmpl_id.name))
