# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    internal_repair = fields.Boolean(
        related="repair_type_id.internal_repair", store=True, copy=False
    )

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
