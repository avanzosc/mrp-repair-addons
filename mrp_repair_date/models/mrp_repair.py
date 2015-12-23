# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    scheduled_departure_date = fields.Date(
        string='Scheduled Departure Date', required=True, copy=False)
    start_date = fields.Date(
        string='Start Date', readonly=True, copy=False)
    end_date = fields.Date(
        string='End Date', readonly=True, copy=False)

    @api.multi
    def action_repair_start(self):
        result = super(MrpRepair, self).action_repair_start()
        self.write({'start_date': fields.Date.context_today(self)})
        return result

    @api.multi
    def action_repair_end(self):
        result = super(MrpRepair, self).action_repair_end()
        self.write({'end_date': fields.Date.context_today(self)})
        return result

    @api.multi
    def action_cancel_draft(self):
        result = super(MrpRepair, self).action_cancel_draft()
        self.write({'start_date': False, 'end_date': False})
        return result
