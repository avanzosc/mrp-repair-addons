# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    partner_invoice_id = fields.Many2one(
        comodel_name="res.partner",
        string="Invoice Address",
        compute="_compute_partner_invoice_id",
        store=True,
        readonly=False,
        required=False,
        precompute=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )

    @api.depends("partner_id")
    def _compute_partner_invoice_id(self):
        for repair in self:
            repair.partner_invoice_id = (
                repair.partner_id.address_get(["invoice"])["invoice"]
                if repair.partner_id
                else False
            )
