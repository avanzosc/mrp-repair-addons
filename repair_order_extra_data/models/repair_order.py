# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    description_breakdown = fields.Text(string="Description breakdown")
    cause = fields.Text()
    repair_made = fields.Text(string="Repair made")
    repairable = fields.Boolean(default=False)
