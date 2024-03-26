# Copyright 2018 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class RepairOrderType(models.Model):
    _name = 'repair.order.type'

    name = fields.Char(string='Repair type', help='Repair order type',
                       translate=True)


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    repair_type_id = fields.Many2one(
        comodel_name='repair.order.type', string='Repair order type')
