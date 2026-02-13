# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class RepairFee(models.Model):
    _inherit = "repair.fee"

    def _get_selection_repair_state(self):
        return self.env["repair.order"].fields_get(allfields=["state"])["state"][
            "selection"
        ]

    repair_state = fields.Selection(
        selection=_get_selection_repair_state,
        related="repair_id.state",
        store=True,
    )
    repair_create_date = fields.Datetime(
        related="repair_id.create_date",
        store=True,
    )
