# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models

from odoo.addons.base.models.res_partner import WARNING_HELP, WARNING_MESSAGE


class ResPartner(models.Model):
    _inherit = "res.partner"

    repair_warn = fields.Selection(
        WARNING_MESSAGE, "Repair Warnings", default="no-message", help=WARNING_HELP
    )
    repair_warn_msg = fields.Text("Message for Repair Order")
