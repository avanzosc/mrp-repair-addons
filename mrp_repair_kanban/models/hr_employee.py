# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def call_wizard_repair_hours(self):
        action = self.env.ref('mrp_repair_kanban.mrp_repair_action_kanban')
        action_dict = action.read()[0] if action else {}
        action_dict.update({'context': {'employee_id': self.id}})
        return action_dict

    @api.multi
    def show_repair_hours(self):
        action = self.env.ref(
            'mrp_repair_kanban.action_repair_employee_pin_view')
        action_dict = action.read()[0] if action else {}
        action_dict.update({'context': {'default_employee_id': self.id,
                                        'default_user_id': self.user_id.id}})
        return action_dict
