# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    def _prepare_production_values(self):
        self.ensure_one()
        values = super()._prepare_production_values()
        if self.claim_id:
            values["claim_id"] = self.claim_id.id
        return values
