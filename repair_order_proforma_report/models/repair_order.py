# Copyright 2015 Esther Martín - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    proforma = fields.Boolean(copy=False)
