# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    internal_repair = fields.Boolean()

    @api.onchange("internal_repair")
    def onchange_internal_claim(self):
        domain = {}
        if self.internal_repair:
            domain = {
                "domain": {
                    "partner_id": [
                        "|",
                        ("id", "=", self.env.company.id),
                        ("parent_id", "=", self.env.company.id),
                    ]
                }
            }
        else:
            domain = {
                "domain": {
                    "partner_id": [
                        ("id", "!=", self.env.company.id),
                        ("parent_id", "!=", self.env.company.id),
                    ]
                }
            }
        return domain

    @api.model_create_multi
    def create(self, vals_list):
        found = False
        for vals in vals_list:
            if "internal_repair" in vals and vals.get("internal_repair", False):
                found = True
        if not found:
            return super().create(vals_list)
        else:
            return super(
                RepairOrder, self.with_context(with_internal_repair_order_sequence=True)
            ).create(vals_list)
