# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, exceptions, fields, models, _
from openerp.addons import decimal_precision as dp
from openerp.models import expression
from openerp.tools.safe_eval import safe_eval


class WizardMrpRepairFee(models.Model):
    _name = 'wizard.mrp.repair.fee'

    @api.model
    def _get_workshop_user(self):
        workshops = self.env['hr.department'].search(
            [('name', 'in', ('Workshop', 'TALLER'))])
        employee_obj = self.env['hr.employee']
        users_lst = employee_obj.search(
            []).filtered(
                lambda r: r.department_id in workshops).mapped('user_id').ids
        return [('id', 'in', users_lst)]

    name = fields.Char(string="Mrp Repair Fee")
    user_id = fields.Many2one(
        comodel_name="res.users", string="Operator", domain=_get_workshop_user)
    description = fields.Text(string="description")
    repair_id = fields.Many2one(
        comodel_name='mrp.repair', string="Repair Order", readonly=True)
    imputation_date = fields.Date(
        string='Imputation Date', default=lambda
        self: fields.Date.context_today(self))
    product_id = fields.Many2one(comodel_name='product.product',
                                 string='Product')
    quantity = fields.Float(
        string='Quantity',
        digits_compute=dp.get_precision('Product Unit of Measure'))
    employee_id = fields.Many2one(comodel_name='hr.employee',
                                  string="Employee")
    pin_code = fields.Integer('PIN')

    @api.multi
    def check_pin(self):
        return self.pin_code == self.user_id.pin_code

    @api.multi
    def save_and_new(self):
        self.add_repair_fee_hour()
        action = self.env.ref('mrp_repair_kanban.mrp_repair_action_kanban')
        action_dict = action.read()[0] if action else {}
        action_dict.update({'context': {'pin_code': self.pin_code}})
        return action_dict

    @api.multi
    def save_and_close(self):
        self.add_repair_fee_hour()
        return self.close_wizard_view()

    @api.multi
    def close_wizard_view(self):
        action = self.env.ref('mrp_repair_kanban.open_view_employee_list_my')
        action_dict = action.read()[0] if action else {}
        action_dict.update({
            'context': {'employee_id': '',
                        'pin_code': ''}})
        return action_dict

    @api.multi
    def add_repair_fee_hour(self):
        fee_line = self.env['mrp.repair.fee']
        if not self.check_pin():
            raise exceptions.Warning(_("Incorrect PIN code"))
        res = fee_line.product_id_change(False, self.product_id.id,
                                         product_uom_qty=self.quantity)
        fee_line_data = {
            'name': self.description or res['value']['name'],
            'product_id': self.product_id.id,
            'imputation_date': self.imputation_date,
            'repair_id': self.repair_id.id,
            'user_id': self.user_id.id,
            'res_partner': self.repair_id.partner_id.id,
            'repair_lot': self.repair_id.lot_id.id,
            'product_uom_qty': res['value']['product_uom_qty'],
            'product_uom': res['value']['product_uom'],
            'price_unit': res['value']['price_unit'],
            'is_from_menu': True,
            }
        fee = fee_line.create(fee_line_data)
        return fee

    @api.multi
    def view_user_repair_hours(self):
        if not self.check_pin():
            raise exceptions.Warning(_("Incorrect PIN code"))
        action = self.env.ref('mrp_repair_kanban.action_mrp_repair_fee')
        action_dict = action.read()[0] if action else {}
        domain = expression.AND([
            [('user_id', '=', self.user_id.id)],
            safe_eval(action.domain or '[]')])
        action_dict.update({'domain': domain,
                            'context': {'search_default_today': 1,
                                        'default_today': 1}})
        return action_dict
