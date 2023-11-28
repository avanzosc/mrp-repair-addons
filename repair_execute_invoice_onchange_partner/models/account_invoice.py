# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def create(self, vals):
        invoice = super(AccountInvoice, self).create(vals)
        if "create_invoice_from_repair" in self.env.context:
            invoice._onchange_partner_id()
        return invoice
