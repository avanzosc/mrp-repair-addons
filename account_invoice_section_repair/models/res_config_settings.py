# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    section_from_repair = fields.Boolean(
        string="In invoices create sections from repairs",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            section_from_repair=(
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("section_from_repair", default=False)
            ),
        )
        return res

    def set_values(self):
        result = super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "section_from_repair", self.section_from_repair
        )
        return result
