# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class RepairLine(models.Model):
    _inherit = "repair.line"

    @api.depends("type")
    def _compute_location_id(self):
        result = super()._compute_location_id()
        for line in self.filtered(lambda x: x.type):
            if (
                line.type == "add"
                and line.location_id
                and not line.location_id.eligible_for_repairs
            ):
                line.location_id = False
            else:
                line.location_id = (
                    line.env["stock.location"]
                    .search(
                        [
                            ("usage", "=", "production"),
                            ("company_id", "=", line.repair_id.company_id.id),
                            ("eligible_for_repairs", "=", True),
                        ],
                        limit=1,
                    )
                    .id
                )
        return result
