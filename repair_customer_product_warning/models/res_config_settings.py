# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_warning_repair = fields.Boolean(
        "Repair Order Warnings",
        implied_group="repair_customer_product_warning.group_warning_repair",
    )
