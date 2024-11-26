# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    @api.onchange("lot_id")
    def _onchange_lot_id(self):
        if self.lot_id and self.lot_id.vehicle_id and self.lot_id.vehicle_id.driver_id:
            self.partner_id = self.lot_id.vehicle_id.driver_id.id
