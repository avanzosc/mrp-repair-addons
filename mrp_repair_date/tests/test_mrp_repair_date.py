# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import odoo.tests.common as common


class TestMrpRepairDate(common.TransactionCase):

    def setUp(self):
        super(TestMrpRepairDate, self).setUp()
        self.data_model = self.env['ir.model.data']
        fee_vals = {'user_id': self.env.ref('base.user_root').id,
                    'name': 'Test mrp repair dates',
                    'product_uom': self.env.ref('product.product_uom_unit').id,
                    'price_unit': 1,
                    'product_uom_qty': 5}
        vals = {'product_id': self.env.ref('product.product_product_8').id,
                'product_uom': self.env.ref('product.product_uom_unit').id,
                'location_id': self.env.ref('stock.stock_location_7').id,
                'location_dest_id': self.env.ref('stock.stock_location_7').id,
                'fees_lines': [(0, 0, fee_vals)]}
        self.repair = self.env['repair.order'].create(vals)

    def test_mrp_repair_date(self):
        self.repair.signal_workflow('repair_confirm')
        self.repair.signal_workflow('repair_ready')
        self.assertNotEqual(
            self.repair.start_date, False,
            'Repair initiated, and is not loaded start date')
        self.repair.action_cancel()
        self.repair.action_cancel_draft()
        self.assertEqual(
            self.repair.start_date, False,
            'Repair to draft, and it did not initialize the value of start '
            'date')
        self.repair.signal_workflow('repair_confirm')
        self.repair.signal_workflow('repair_ready')
        self.repair.signal_workflow('action_repair_end')
        self.assertNotEqual(
            self.repair.end_date, False,
            'Repair finished, and is not loaded end date')
