# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models

QUOTATION_STATES = ['draft']


class WizMrpRepairCancelReason(models.TransientModel):
    _name = 'mrp.repair.cancel'
    _description = 'Ask a reason from the repair cancellation'

    reason_id = fields.Many2one(
        comodel_name='mrp.repair.cancel.reason', string='Reason',
        required=True)

    @api.multi
    def confirm_cancel(self):
        self.ensure_one()
        act_close = {'type': 'ir.actions.act_window_close'}
        repair_ids = self.env.context.get('active_ids', False)
        if not repair_ids:
            return act_close
        assert len(repair_ids) == 1, "Only 1 repair ID expected"
        repair = self.env['mrp.repair'].browse(repair_ids)
        repair.cancel_reason_id = self.reason_id.id
        if repair.state in QUOTATION_STATES:
            repair.signal_workflow('cancel')
        else:
            repair.action_cancel()
        return act_close
