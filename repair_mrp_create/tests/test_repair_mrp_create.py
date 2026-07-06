# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestRepairMrpCreate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)], limit=1
        )
        # Product that will be manufactured from the repair's bill of materials.
        cls.product = cls.env["product.product"].create(
            {
                "name": "Repairable Product",
                "type": "consu",
                "is_storable": True,
            }
        )
        cls.component = cls.env["product.product"].create(
            {
                "name": "Repair Component",
                "type": "consu",
                "is_storable": True,
            }
        )
        # Bill of materials eligible in repairs.
        cls.bom = cls.env["mrp.bom"].create(
            {
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "product_qty": 1.0,
                "product_uom_id": cls.uom_unit.id,
                "type": "normal",
                "eligible_in_repairs": True,
            }
        )
        # Bill of materials NOT eligible in repairs (used for the domain test).
        cls.bom_not_eligible = cls.env["mrp.bom"].create(
            {
                "product_tmpl_id": cls.component.product_tmpl_id.id,
                "product_qty": 1.0,
                "product_uom_id": cls.uom_unit.id,
                "type": "normal",
                "eligible_in_repairs": False,
            }
        )
        cls.repair = cls.env["repair.order"].create(
            {
                "product_id": cls.product.id,
                "product_uom": cls.uom_unit.id,
                "picking_type_id": cls.warehouse.repair_type_id.id,
            }
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _create_production(self, repair=None, bom=None):
        repair = repair or self.repair
        repair.bom_id = bom or self.bom
        action = repair.action_create_production()
        return self.env["mrp.production"].browse(action["res_id"])

    # ------------------------------------------------------------------
    # Bill of materials
    # ------------------------------------------------------------------
    def test_bom_eligible_field(self):
        self.assertTrue(self.bom.eligible_in_repairs)
        self.assertFalse(self.bom_not_eligible.eligible_in_repairs)

    def test_bom_id_domain_only_eligible(self):
        """The bom_id field must only accept boms eligible in repairs."""
        field = self.env["repair.order"]._fields["bom_id"]
        self.assertIn("eligible_in_repairs", field.domain)
        eligible = self.env["mrp.bom"].search([("eligible_in_repairs", "=", True)])
        self.assertIn(self.bom, eligible)
        self.assertNotIn(self.bom_not_eligible, eligible)

    # ------------------------------------------------------------------
    # Create MO
    # ------------------------------------------------------------------
    def test_create_production_without_bom_raises(self):
        self.repair.bom_id = False
        with self.assertRaises(UserError):
            self.repair.action_create_production()

    def test_create_production_values(self):
        production = self._create_production()
        self.assertEqual(production.product_id, self.product)
        self.assertEqual(production.product_qty, 1.0)
        self.assertEqual(production.bom_id, self.bom)
        self.assertEqual(production.repair_id, self.repair)
        self.assertEqual(production.origin, self.repair.name)
        self.assertEqual(production.company_id, self.company)
        # Locations and operation type are set explicitly so the MO is always
        # created with the required locations.
        self.assertTrue(production.picking_type_id)
        self.assertTrue(production.location_src_id)
        self.assertTrue(production.location_dest_id)

    def test_create_production_links_repair(self):
        production = self._create_production()
        self.assertIn(production, self.repair.production_ids)
        self.assertEqual(self.repair.production_count, 1)

    def test_create_production_returns_form_action(self):
        existing = self.env["mrp.production"].search(
            [("repair_id", "=", self.repair.id)]
        )
        self.repair.bom_id = self.bom
        action = self.repair.action_create_production()
        new_production = self.env["mrp.production"].browse(action["res_id"])
        self.assertEqual(action["res_model"], "mrp.production")
        self.assertNotIn(new_production, existing)
        self.assertEqual(new_production.repair_id, self.repair)
        self.assertEqual(action["context"]["default_repair_id"], self.repair.id)

    # ------------------------------------------------------------------
    # Smart button navigation
    # ------------------------------------------------------------------
    def test_action_view_productions_single(self):
        production = self._create_production()
        action = self.repair.action_view_productions()
        self.assertEqual(action["res_id"], production.id)
        self.assertEqual(action["views"], [(False, "form")])

    def test_action_view_productions_multiple(self):
        self._create_production()
        self._create_production()
        action = self.repair.action_view_productions()
        self.assertEqual(self.repair.production_count, 2)
        self.assertEqual(action["domain"], [("repair_id", "=", self.repair.id)])
        # With several MOs the action must not target a single record.
        self.assertFalse(action.get("res_id"))

    # ------------------------------------------------------------------
    # Button visibility helper fields
    # ------------------------------------------------------------------
    def test_flags_without_production(self):
        self.assertFalse(self.repair.has_open_production)
        self.assertFalse(self.repair.has_done_production)

    def test_flags_with_draft_production(self):
        production = self._create_production()
        self.assertEqual(production.state, "draft")
        # An open (not cancelled) MO hides the "Create MO" button.
        self.assertTrue(self.repair.has_open_production)
        # No done MO yet, so the "Cancel" button stays available.
        self.assertFalse(self.repair.has_done_production)

    def test_flags_with_confirmed_production(self):
        production = self._create_production()
        production.action_confirm()
        self.assertEqual(production.state, "confirmed")
        self.assertTrue(self.repair.has_open_production)
        self.assertFalse(self.repair.has_done_production)

    def test_flags_with_cancelled_production(self):
        """A cancelled MO must free the 'Create MO' button again."""
        production = self._create_production()
        production.action_confirm()
        production.action_cancel()
        self.assertEqual(production.state, "cancel")
        self.assertFalse(self.repair.has_open_production)
        self.assertFalse(self.repair.has_done_production)

    def test_flags_with_done_production(self):
        production = self._create_production()
        # Force the done state to simulate a completed MO without running the
        # full manufacturing flow (state is preserved by mrp's compute).
        production.write({"state": "done"})
        production.flush_recordset()
        self.assertEqual(production.state, "done")
        # A done MO is finished, not open: it must NOT block "Create MO"
        # (it is treated like a cancelled one).
        self.assertFalse(self.repair.has_open_production)
        # "Cancel" must be hidden because of the done MO.
        self.assertTrue(self.repair.has_done_production)

    def test_flags_with_done_and_open_productions(self):
        """A done MO does not block, but an in-progress one still does."""
        done_prod = self._create_production()
        done_prod.write({"state": "done"})
        done_prod.flush_recordset()
        open_prod = self._create_production()
        self.assertEqual(open_prod.state, "draft")
        # There is still an open MO -> "Create MO" hidden.
        self.assertTrue(self.repair.has_open_production)
        # And there is a done MO -> "Cancel" hidden.
        self.assertTrue(self.repair.has_done_production)

    def test_flags_with_cancelled_and_done_productions(self):
        """All MOs finished (cancelled or done) -> 'Create MO' available."""
        cancelled = self._create_production()
        cancelled.action_confirm()
        cancelled.action_cancel()
        done_prod = self._create_production()
        done_prod.write({"state": "done"})
        done_prod.flush_recordset()
        self.assertEqual(cancelled.state, "cancel")
        self.assertEqual(done_prod.state, "done")
        # No open MO -> "Create MO" available again...
        self.assertFalse(self.repair.has_open_production)
        # ...but there is a done MO -> "Cancel" still hidden.
        self.assertTrue(self.repair.has_done_production)

    def test_flags_with_mixed_productions(self):
        open_prod = self._create_production()
        cancelled = self._create_production()
        cancelled.action_confirm()
        cancelled.action_cancel()
        self.assertEqual(open_prod.state, "draft")
        self.assertEqual(cancelled.state, "cancel")
        # One MO is still open, so "Create MO" is hidden.
        self.assertTrue(self.repair.has_open_production)
        self.assertFalse(self.repair.has_done_production)

    def test_flags_with_all_cancelled_productions(self):
        first = self._create_production()
        second = self._create_production()
        (first + second).action_confirm()
        (first + second).action_cancel()
        self.assertEqual(set((first + second).mapped("state")), {"cancel"})
        # All MOs cancelled -> "Create MO" available again.
        self.assertFalse(self.repair.has_open_production)
        self.assertFalse(self.repair.has_done_production)

    # ------------------------------------------------------------------
    # repair_id propagation to work orders and productivity logs
    # ------------------------------------------------------------------
    def test_repair_id_propagation(self):
        production = self._create_production()
        workcenter = self.env["mrp.workcenter"].create({"name": "Test WC"})
        workorder = self.env["mrp.workorder"].create(
            {
                "name": "Test WO",
                "production_id": production.id,
                "workcenter_id": workcenter.id,
                "product_uom_id": self.uom_unit.id,
            }
        )
        self.assertEqual(workorder.repair_id, self.repair)
        productivity = self.env["mrp.workcenter.productivity"].create(
            {
                "workorder_id": workorder.id,
                "workcenter_id": workcenter.id,
                "loss_id": self.env.ref("mrp.block_reason0").id,
            }
        )
        self.assertEqual(productivity.repair_id, self.repair)

    # ------------------------------------------------------------------
    # View integrity: the inherited repair form must stay valid.
    # ------------------------------------------------------------------
    def test_repair_form_view_loads(self):
        view = self.env.ref("repair_mrp_create.view_repair_order_form")
        arch = self.env["repair.order"].get_view(view.id, "form")["arch"]
        self.assertIn("action_create_production", arch)
        self.assertIn("has_open_production", arch)
        self.assertIn("has_done_production", arch)
