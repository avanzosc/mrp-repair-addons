# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    @api.model
    def next_by_code(self, sequence_code, sequence_date=None):
        if (
            sequence_code == "repair.order"
            and "with_internal_repair_order_sequence" in self.env.context
        ):
            return super().next_by_code(
                "repair.order.internal", sequence_date=sequence_date
            )
        return super().next_by_code(sequence_code, sequence_date=sequence_date)
