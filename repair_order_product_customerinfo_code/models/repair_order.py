# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    customer_product_code = fields.Char(
        compute="_compute_customer_product_code", store=True, copy=False
    )

    @api.depends(
        "partner_id",
        "product_id",
        "product_id.variant_customer_ids",
        "product_id.variant_customer_ids.product_code",
    )
    def _compute_customer_product_code(self):
        for repair in self:
            if not repair.partner_id or not repair.product_id:
                repair.customer_product_code = ""
            else:
                customer = repair.product_id._select_customerinfo(repair.partner_id)
                repair.customer_product_code = customer.product_code
