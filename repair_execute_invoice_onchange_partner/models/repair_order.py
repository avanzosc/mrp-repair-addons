# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    @api.multi
    def action_invoice_create(self, group=False):
        return super(RepairOrder, self.with_context(
            create_invoice_from_repair=True)).action_invoice_create(group=group)
