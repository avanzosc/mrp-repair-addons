# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestMrpRepairCancelReason(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairCancelReason, self).setUp()
        self.data_model = self.env['ir.model.data']
        self.repair_order_model = self.env['repair.order']
        self.wiz_model = self.env['wiz.repair.order.cancel.reason']
        self.product = self.env.ref('product.product_product_6')
        self.warehouse = self.data_model.get_object('stock', 'warehouse0')
        vals = {'product_id': self.product.id,
                'location_id': self.warehouse.lot_stock_id.id,
                'location_dest_id': self.warehouse.lot_stock_id.id,
                'product_uom': self.product.uom_id.id}
        self.repair_order = self.repair_order_model.create(vals)
        self.reason = self.env.ref(
            'repair_order_cancel_reason.mrp_cancel_reason_customer')

    def test_wizard_cancel_draft_repair_with_reason(self):
        vals = {'reason_id': self.reason.id}
        wiz = self.wiz_model.create(vals)
        wiz.with_context(active_ids=[self.repair_order.id]).confirm_cancel()
        self.assertEqual(
            self.repair_order.state, 'cancel',
            'Repair order not in CANCEL state')
        self.assertEqual(
            self.repair_order.cancel_reason_id.id, self.reason.id,
            'Repair order canceled without cancel reason')

    def test_wizard_cancel_confirmed_repair_with_reason(self):
        self.repair_order.signal_workflow('repair_confirm')
        vals = {'reason_id': self.reason.id}
        wiz = self.wiz_model.create(vals)
        wiz.with_context(active_ids=[self.repair_order.id]).confirm_cancel()
        self.assertEqual(
            self.repair_order.state, 'cancel',
            'Confirmed Repair order not in CANCEL state')
        self.assertEqual(
            self.repair_order.cancel_reason_id.id, self.reason.id,
            'Confirmed Repair order canceled without cancel reason')
