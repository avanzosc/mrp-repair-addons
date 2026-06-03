# Copyright 2025 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    vehicle_id = fields.Many2one(
        "fleet.vehicle",
        string="Vehicle",
        related="lot_id.vehicle_id",
        store=True,
        readonly=False,
    )

    vehicle_brand = fields.Char(
        related="vehicle_id.model_id.brand_id.name", string="Brand", readonly=True
    )
    vehicle_model = fields.Char(
        related="vehicle_id.model_id.name", string="Model", readonly=True
    )
    vehicle_license_plate = fields.Char(
        related="vehicle_id.license_plate", string="License_plate", readonly=True
    )
    vehicle_vin = fields.Char(
        related="vehicle_id.vin_sn", string="Vin sn", readonly=True
    )

    odometer_km = fields.Float(string="Km")
    fuel_level = fields.Selection(
        [
            ("1_4", "1/4"),
            ("1_2", "1/2"),
            ("3_4", "3/4"),
            ("full", "Lleno"),
        ],
        string="Fuel level",
    )

    @api.onchange("vehicle_id")
    def _onchange_vehicle_id_set_partner(self):
        if self.vehicle_id and self.vehicle_id.driver_id:
            self.partner_id = self.vehicle_id.driver_id.id


    def action_repair_done(self):
        res = super().action_repair_done()
        for rec in self:
            if rec.vehicle_id and rec.odometer_km:
                rec.env["fleet.vehicle.odometer"].create(
                    {
                        "vehicle_id": rec.vehicle_id.id,
                        "value": rec.odometer_km,
                        "date": fields.Datetime.now(),
                        "driver_id": rec.partner_id.id if rec.partner_id else False,
                    }
                )
        return res