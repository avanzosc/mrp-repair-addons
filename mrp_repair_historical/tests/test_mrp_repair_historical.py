# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import odoo.tests.common as common
from odoo import fields


class TestMrpRepairHistorical(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.repair_model = self.env["repair.order"]
        self.supplierinfo_model = self.env["product.supplierinfo"]
        self.supplier = self.env.ref("base.partner_root")
        self.product = self.env["product.template"].create(
            {
                "name": "Product",
                "default_code": "CODE",
            }
        )
        self.supplierinfo = self.supplierinfo_model.create(
            {
                "name": self.supplier.id,
                "product_tmpl_id": self.product.id,
                "product_code": "SUP CODE",
                "product_name": "Product Name",
            }
        )

    def test_mrp_repair_historical(self):
        suppinfo = self.supplierinfo_model.name_search("CODE")
        self.assertEqual(self.supplierinfo.name_get(), suppinfo)
        self.assertEqual(self.supplierinfo.display_name, self.supplierinfo.name.name)
        self.assertEqual(
            self.supplierinfo.with_context(
                show_customer_product_code=True
            ).display_name,
            "[{}] {}".format(
                self.supplierinfo.product_code, self.supplierinfo.product_name
            ),
        )
        self.supplierinfo.write(
            {
                "product_code": "",
                "product_name": "Product Name",
            }
        )
        self.supplierinfo.invalidate_cache()
        self.assertEqual(
            self.supplierinfo.with_context(
                show_customer_product_code=True
            ).display_name,
            "[{}] {}".format(
                self.supplierinfo.product_tmpl_id.default_code,
                self.supplierinfo.product_name,
            ),
        )
        self.supplierinfo.write(
            {
                "product_code": "SUP CODE",
                "product_name": "",
            }
        )
        self.supplierinfo.invalidate_cache()
        self.assertEqual(
            self.supplierinfo.with_context(
                show_customer_product_code=True
            ).display_name,
            "[{}] {}".format(
                self.supplierinfo.product_code, self.supplierinfo.product_tmpl_id.name
            ),
        )
        self.supplierinfo.write(
            {
                "product_code": "",
                "product_name": "",
            }
        )
        self.supplierinfo.invalidate_cache()
        self.assertEqual(
            self.supplierinfo.with_context(
                show_customer_product_code=True
            ).display_name,
            "[{}] {}".format(
                self.supplierinfo.product_tmpl_id.default_code,
                self.supplierinfo.product_tmpl_id.name,
            ),
        )

    def test_mrp_repair_historical_date_repair(self):
        self.repair = self.repair_model.search([], limit=1)
        self.repair.write(
            {"customer_lot_ids": [(0, 0, {"product_code": self.supplierinfo.id})]}
        )
        self.assertEqual(
            fields.Datetime.from_string(self.repair.date_repair).date(),
            fields.Date.from_string(self.repair.customer_lot_ids[0].date_repair),
        )
