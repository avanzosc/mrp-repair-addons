# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    def _create_invoices(self, group=False):
        return super(
            RepairOrder, self.with_context(from_repair_order=True)
        )._create_invoices(group=group)
