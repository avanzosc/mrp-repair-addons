# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class RepairOrder(models.Model):
    _inherit = 'repair.order'

    finished_task = fields.Boolean(
        string='Finished task', default=False)

    def action_task_end(self):
        for repair in self:
            repair.finished_task = True

    def action_cancel_validation(self):
        for repair in self:
            repair.write({'finished_task': False,
                          'state': 'under_repair'})
