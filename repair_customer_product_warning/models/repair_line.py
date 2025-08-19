# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, models


class RepairLine(models.Model):
    _inherit = "repair.line"

    @api.onchange("product_id")
    def _onchange_product_id_warning(self):
        if not self.product_id:
            return

        product = self.product_id
        if product.repair_line_warn != "no-message":
            if product.repair_line_warn == "block":
                self.product_id = False

            return {
                "warning": {
                    "title": _("Warning for %s", product.name),
                    "message": product.repair_line_warn_msg,
                }
            }
