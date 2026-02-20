# Copyright 2026 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class RepairFee(models.Model):
    _inherit = "repair.fee"

    repair_state = fields.Selection(
        related="repair_id.state",
        store=True,
    )
    repair_create_date = fields.Datetime(
        string="Repair Create Date",
        related="repair_id.create_date",
        store=True,
    )
