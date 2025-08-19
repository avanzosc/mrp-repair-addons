# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    @api.onchange("partner_id")
    def _onchange_partner_id_warning(self):
        if not self.partner_id:
            return

        partner = self.partner_id

        # If partner has no warning, check its company
        if partner.repair_warn == "no-message" and partner.parent_id:
            partner = partner.parent_id

        if partner.repair_warn and partner.repair_warn != "no-message":
            # Block if partner only has warning but parent company is blocked
            if (
                partner.repair_warn != "block"
                and partner.parent_id
                and partner.parent_id.repair_warn == "block"
            ):
                partner = partner.parent_id

            if partner.repair_warn == "block":
                self.partner_id = False

            return {
                "warning": {
                    "title": _("Warning for %s", partner.name),
                    "message": partner.repair_warn_msg,
                }
            }

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
