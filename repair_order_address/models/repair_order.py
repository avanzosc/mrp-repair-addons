# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    address_id = fields.Many2one(
        string="Delivery Address",
        comodel_name="res.partner",
        domain="[('parent_id','=',partner_id)]",
        check_company=True,
    )
