# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestMrpRepairPartnerAnalytic(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairPartnerAnalytic, self).setUp()
        self.product = self.env.ref('product.product_product_6')
        self.warehouse = self.env['ir.model.data'].get_object('stock',
                                                              'warehouse0')
        self.analytic_default_model = self.env['account.analytic.default']
        vals = {
            'name': 'Test Customer',
            'is_company': True,
            'customer': True,
            'company_id': self.env.user.company_id.id,
        }
        self.customer = self.env['res.partner'].create(vals)
        vals = {'name': 'test',
                'product_id': self.product.id,
                'location_id': self.warehouse.lot_stock_id.id,
                'location_dest_id': self.warehouse.lot_stock_id.id,
                'product_uom': self.product.uom_id.id,
                'partner_id': self.customer.id}
        self.mrp_repair = self.env['mrp.repair'].create(vals)

    def test_mrp_repair_partner_analytic(self):
        self.assertNotEqual(
            self.mrp_repair.analytic_account, False,
            'Not generated analytic account for repair')
