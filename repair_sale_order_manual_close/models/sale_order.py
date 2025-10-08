# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _change_repair_order_status_done(self):
        manual_close = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("repair_sale_order_manual_close.close_repair_manually")
        )
        if not manual_close:
            return super()._change_repair_order_status_done()
        return True
