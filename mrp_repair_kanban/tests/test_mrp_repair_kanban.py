# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import openerp.tests.common as common
from openerp import exceptions


class TestRepairKanban(common.TransactionCase):

    def setUp(self):
        super(TestRepairKanban, self).setUp()
        employee_model = self.env['hr.employee']
        employee_vals = {
            'name': 'employee name',
            'user_id': self.ref('base.user_root'),
        }
        employee_vals.update(
            employee_model.onchange_user(
                user_id=employee_vals['user_id'])['value'])
        self.employee = employee_model.create(employee_vals)
        self.wiz_obj = self.env['wizard.mrp.repair.fee']
        self.mrp_repair_model = self.env['mrp.repair']
        self.product = self.browse_ref('product.product_product_3')
        self.location = self.ref('stock.location_inventory')
        self.partner = self.env.ref('base.res_partner_1')
        self.customer = self.env['res.partner'].create({
            'name': 'Test Customer',
            'is_company': True,
            'customer': True,
            'company_id': self.env.user.company_id.id,
        })
        vals = {'name': 'test',
                'product_id': self.product.id,
                'location_id': self.location,
                'location_dest_id': self.location,
                'product_uom': self.product.uom_id.id,
                'partner_id': self.customer.id}
        self.mrp_repair_customer = self.env['mrp.repair'].create(vals)

    def test_employee_call_wizard_repair_hours(self):
        self.employee.user_id.pin_code = 9999
        data = self.employee.call_wizard_repair_hours()
        self.assertEqual(data['context']['employee_id'],
                         self.employee.id, 'Employee_id is not not the same.')
        wizard = self.wiz_obj.with_context(
            default_employee_id=self.employee.id,
            default_user_id=self.employee.user_id.id).create({})
        with self.assertRaises(exceptions.Warning):
            wizard.view_user_repair_hours()
        wizard.write({'pin_code': 9999})
        data2 = wizard.view_user_repair_hours()
        self.assertEqual(data2['domain'],
                         [('user_id', '=', self.employee.user_id.id)],
                         'Data do not match')

    def test_employee_show_repair_hours(self):
        data = self.employee.show_repair_hours()
        self.assertEqual(data['context']['default_employee_id'],
                         self.employee.id, 'Employee is not not the same.')

    def test_repair_call_wizard_repair_hours(self):
        data = self.mrp_repair_customer.with_context(
            employee_id=self.employee.id).call_wizard_repair_hours()
        self.assertTrue(data['res_id'])

    def test_mrp_repair_wizard(self):
        self.employee.user_id.pin_code = 9999
        data = self.mrp_repair_customer.with_context(
            employee_id=self.employee.id).call_wizard_repair_hours()
        wizard = self.wiz_obj.browse(data['res_id'])
        self.assertNotEqual(wizard.check_pin(), True)
        with self.assertRaises(exceptions.Warning):
            wizard.save_and_new()
        wizard.write({'pin_code': 9999,
                      'description': 'New Fee Line',
                      'quantity': 2,
                      })
        data2 = wizard.save_and_new()
        self.assertEqual(data2['context']['pin_code'], 9999)
        data3 = wizard.save_and_close()
        self.assertEqual(data3['context']['pin_code'], '')
