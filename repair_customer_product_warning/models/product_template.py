# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models

from odoo.addons.base.models.res_partner import WARNING_HELP, WARNING_MESSAGE


class ProductTemplate(models.Model):
    _inherit = "product.template"

    repair_line_warn = fields.Selection(
        WARNING_MESSAGE,
        "Repair Line",
        default="no-message",
        help=WARNING_HELP,
        required=True,
    )
    repair_line_warn_msg = fields.Text("Message for Repair Line")
