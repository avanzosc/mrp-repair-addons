# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    @api.multi
    def call_wizard_repair_hours(self):
        wiz_obj = self.env['wizard.mrp.repair.fee']
        employee_obj = self.env['hr.employee']
        employee_id = self.env.context.get('employee_id', False)
        pin_code = self.env.context.get('pin_code', False)
        if employee_id:
            employee = employee_obj.browse(employee_id)
            wiz_data = {
                'repair_id': self.id,
                'user_id': employee.user_id.id,
                'product_id': employee.product_id.id,
                'pin_code': pin_code,
            }
            wizard = wiz_obj.create(wiz_data)
        action = self.env.ref('mrp_repair_kanban.action_wizard_mrp_repair_fee')
        action_dict = action.read()[0] if action else {}
        action_dict.update({'res_id': wizard.id})
        return action_dict
