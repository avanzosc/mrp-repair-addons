# Copyright 2018 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class MrpRepairType(models.Model):
    _name = 'mrp.repair.type'

    name = fields.Char(string='Repair type', help='Repair order type',
                       translate=True)


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    repair_type_id = fields.Many2one(
        comodel_name='mrp.repair.type', string='Repair order type')
