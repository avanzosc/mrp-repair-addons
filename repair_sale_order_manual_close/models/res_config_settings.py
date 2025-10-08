# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    repair_close_manual = fields.Boolean(
        string="Do not close repair order on sale confirmation",
        config_parameter="repair_sale_order_manual_close.close_repair_manually",
    )
