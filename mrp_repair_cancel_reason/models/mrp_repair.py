# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    cancel_reason_id = fields.Many2one(
        'mrp.repair.cancel.reason', string='Reason for cancellation',
        readonly=True, ondelete='restrict')


class MrpRepairCancelReason(models.Model):
    _name = 'mrp.repair.cancel.reason'
    _description = 'Repair Cancel Reason'

    name = fields.Char('Reason', required=True, translate=True)
