# Copyright 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.exceptions import UserError
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestMrpRepairCancelReason(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wiz_model = cls.env["wiz.repair.order.cancel.reason"]
        cls.reason = cls.env.ref("mrp_repair_cancel_reason.mrp_cancel_reason_customer")

        # Partners
        cls.res_partner_1 = cls.env["res.partner"].create({"name": "Wood Corner"})
        cls.res_partner_address_1 = cls.env["res.partner"].create(
            {"name": "Willie Burke", "parent_id": cls.res_partner_1.id}
        )
        cls.res_partner_12 = cls.env["res.partner"].create({"name": "Partner 12"})

        # Products
        cls.product_product_3 = cls.env["product.product"].create(
            {"name": "Desk Combination"}
        )
        cls.product_product_11 = cls.env["product.product"].create(
            {"name": "Conference Chair"}
        )
        cls.product_product_5 = cls.env["product.product"].create({"name": "Product 5"})
        cls.product_product_6 = cls.env["product.product"].create(
            {"name": "Large Cabinet"}
        )
        cls.product_product_12 = cls.env["product.product"].create(
            {"name": "Office Chair Black"}
        )
        cls.product_product_13 = cls.env["product.product"].create(
            {"name": "Corner Desk Left Sit"}
        )
        cls.product_product_2 = cls.env["product.product"].create(
            {"name": "Virtual Home Staging"}
        )
        cls.product_service_order_repair = cls.env["product.product"].create(
            {
                "name": "Repair Services",
                "type": "service",
            }
        )

        # Location
        cls.stock_warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.company.id)], limit=1
        )
        cls.stock_location_14 = cls.env["stock.location"].create(
            {
                "name": "Shelf 2",
                "location_id": cls.stock_warehouse.lot_stock_id.id,
            }
        )

        # Repair Orders
        cls.repair1 = cls.env["repair.order"].create(
            {
                "address_id": cls.res_partner_address_1.id,
                "guarantee_limit": "2019-01-01",
                "invoice_method": "none",
                "user_id": False,
                "product_id": cls.product_product_3.id,
                "product_uom": cls.env.ref("uom.product_uom_unit").id,
                "partner_invoice_id": cls.res_partner_address_1.id,
                "location_id": cls.stock_warehouse.lot_stock_id.id,
                "operations": [
                    (
                        0,
                        0,
                        {
                            "location_dest_id": (
                                cls.product_product_11.property_stock_production.id
                            ),
                            "location_id": cls.stock_warehouse.lot_stock_id.id,
                            "name": cls.product_product_11.name,
                            "product_id": cls.product_product_11.id,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "product_uom_qty": 1.0,
                            "price_unit": 50.0,
                            "state": "draft",
                            "type": "add",
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "fees_lines": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product_service_order_repair.name,
                            "product_id": cls.product_service_order_repair.id,
                            "product_uom_qty": 1.0,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 50.0,
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "partner_id": cls.res_partner_12.id,
            }
        )

        cls.repair0 = cls.env["repair.order"].create(
            {
                "product_id": cls.product_product_5.id,
                "product_uom": cls.env.ref("uom.product_uom_unit").id,
                "address_id": cls.res_partner_address_1.id,
                "invoice_method": "after_repair",
                "partner_invoice_id": cls.res_partner_address_1.id,
                "location_id": cls.stock_warehouse.lot_stock_id.id,
                "operations": [
                    (
                        0,
                        0,
                        {
                            "location_dest_id": (
                                cls.product_product_12.property_stock_production.id
                            ),
                            "location_id": cls.stock_warehouse.lot_stock_id.id,
                            "name": cls.product_product_12.name,
                            "price_unit": 50.0,
                            "product_id": cls.product_product_12.id,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "product_uom_qty": 1.0,
                            "state": "draft",
                            "type": "add",
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "fees_lines": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product_service_order_repair.name,
                            "product_id": cls.product_service_order_repair.id,
                            "product_uom_qty": 1.0,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 50.0,
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "partner_id": cls.res_partner_12.id,
            }
        )

        cls.repair2 = cls.env["repair.order"].create(
            {
                "product_id": cls.product_product_6.id,
                "product_uom": cls.env.ref("uom.product_uom_unit").id,
                "address_id": cls.res_partner_address_1.id,
                "invoice_method": "b4repair",
                "partner_invoice_id": cls.res_partner_address_1.id,
                "location_id": cls.stock_location_14.id,
                "operations": [
                    (
                        0,
                        0,
                        {
                            "location_dest_id": (
                                cls.product_product_13.property_stock_production.id
                            ),
                            "location_id": cls.stock_warehouse.lot_stock_id.id,
                            "name": cls.product_product_13.name,
                            "price_unit": 50.0,
                            "product_id": cls.product_product_13.id,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "product_uom_qty": 1.0,
                            "state": "draft",
                            "type": "add",
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "fees_lines": [
                    (
                        0,
                        0,
                        {
                            "name": cls.product_service_order_repair.name,
                            "product_id": cls.product_service_order_repair.id,
                            "product_uom_qty": 1.0,
                            "product_uom": cls.env.ref("uom.product_uom_unit").id,
                            "price_unit": 50.0,
                            "company_id": cls.env.company.id,
                        },
                    )
                ],
                "partner_id": cls.res_partner_12.id,
            }
        )

        cls.env.user.groups_id |= cls.env.ref("stock.group_stock_user")

    def test_no_invoice_cancel_under_repair(self):
        self.assertEqual(
            self.repair1.invoice_method,
            "none",
            "Repair order invoice method should be 'none'",
        )
        self.repair1.action_repair_confirm()
        self.repair1.action_repair_start()
        self.assertEqual(
            self.repair1.state,
            "under_repair",
            "Repair order should be in 'under_repair' state",
        )
        vals = {"reason_id": self.reason.id}
        wiz = self.wiz_model.create(vals)
        wiz.with_context(active_ids=[self.repair1.id]).confirm_cancel()
        self.assertEqual(
            self.repair1.state, "cancel", "Repair order should be in 'cancel' state"
        )
        self.assertEqual(
            self.repair1.cancel_reason_id.id,
            self.reason.id,
            "Repair order should have a cancel reason",
        )
        self.repair1.action_repair_cancel_draft()
        self.assertFalse(
            self.repair1.cancel_reason_id.id,
            "Repair order should have erased cancel reason",
        )

    def test_no_invoice_cancel_done(self):
        self.assertEqual(
            self.repair1.invoice_method,
            "none",
            "Repair order invoice method should be 'none'",
        )
        self.repair1.action_repair_confirm()
        self.repair1.action_repair_start()
        self.repair1.action_repair_end()
        self.assertEqual(
            self.repair1.state, "done", "Repair order should be in 'done' state"
        )
        vals = {"reason_id": self.reason.id}
        wiz = self.wiz_model.create(vals)
        with self.assertRaises(UserError):
            wiz.with_context(active_ids=[self.repair1.id]).confirm_cancel()

    def test_cancel_b4repair_under_repair(self):
        self.assertEqual(
            self.repair2.invoice_method,
            "b4repair",
            "Repair order invoice method should be 'b4repair'",
        )
        self.repair2.action_repair_confirm()
        self.repair2.action_repair_invoice_create()
        self.repair2.action_repair_start()
        self.assertEqual(
            self.repair2.state,
            "under_repair",
            "Repair order should be in 'under_repair' state",
        )
        vals = {"reason_id": self.reason.id}
        wiz = self.wiz_model.create(vals)
        wiz.with_context(active_ids=[self.repair2.id]).confirm_cancel()
        self.assertEqual(
            self.repair2.state,
            "cancel",
            "Repair order should be in 'cancel' state",
        )
        self.assertEqual(
            self.repair2.cancel_reason_id.id,
            self.reason.id,
            "Repair order should have a cancel reason",
        )

    def test_cancel_b4repair_done(self):
        self.assertEqual(
            self.repair2.invoice_method,
            "b4repair",
            "Repair order invoice method should be 'b4repair'",
        )
        self.repair2.action_repair_confirm()
        self.repair2.action_repair_invoice_create()
        self.repair2.action_repair_start()
        self.repair2.action_repair_end()
        self.assertEqual(
            self.repair2.state, "done", "Repair order should be in 'done' state"
        )
        vals = {"reason_id": self.reason.id}
        wiz = self.wiz_model.create(vals)
        with self.assertRaises(UserError):
            wiz.with_context(active_ids=[self.repair2.id]).confirm_cancel()

    def test_cancel_after_repair_under_repair(self):
        self.assertEqual(
            self.repair0.invoice_method,
            "after_repair",
            "Repair order invoice method should be 'after_repair'",
        )
        self.repair0.action_repair_confirm()
        self.repair0.action_repair_start()
        self.assertEqual(
            self.repair0.state,
            "under_repair",
            "Repair order should be in 'under_repair' state",
        )
        vals = {"reason_id": self.reason.id}
        wiz = self.wiz_model.create(vals)
        wiz.with_context(active_ids=[self.repair0.id]).confirm_cancel()
        self.assertEqual(
            self.repair0.state,
            "cancel",
            "Repair order should be in 'cancel' state",
        )
        self.assertEqual(
            self.repair0.cancel_reason_id.id,
            self.reason.id,
            "Repair order should have a cancel reason",
        )

    def test_cancel_after_repair_done(self):
        self.assertEqual(
            self.repair0.invoice_method,
            "after_repair",
            "Repair order invoice method should be 'after_repair'",
        )
        self.repair0.action_repair_confirm()
        self.repair0.action_repair_start()
        self.repair0.action_repair_end()
        self.assertEqual(
            self.repair0.state,
            "2binvoiced",
            "Repair order should be in '2binvoiced' state",
        )
        vals = {"reason_id": self.reason.id}
        wiz = self.wiz_model.create(vals)
        with self.assertRaises(UserError):
            wiz.with_context(active_ids=[self.repair0.id]).confirm_cancel()
