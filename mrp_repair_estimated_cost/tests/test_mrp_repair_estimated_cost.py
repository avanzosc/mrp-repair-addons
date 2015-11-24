# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.mrp_repair_analytic.tests.test_mrp_repair_analytic import (
    TestMrpRepairAnalytic)
from openerp import exceptions


class TestMrpRepairAnalytic(TestMrpRepairAnalytic):

    def test_mrp_repair_create_cost_no_journal(self):
        self.env.ref('mrp.analytic_journal_repair').unlink()
        with self.assertRaises(exceptions.Warning):
            self.mrp_repair.signal_workflow('repair_confirm')

    def test_mrp_repair_cero_amount_cost(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        self.mrp_repair.create_repair_cost()
        self.op_product.standard_price = 0
        ope_line = self.analytic_line_model.search(
            [('account_id', '=', self.analytic_id.id),
             ('product_id', '=', self.op_product.id),
             ('is_repair_cost', '=', True),
             ('repair_estim_amount', '=', 0),
             ('amount', '=', 0)])
        self.assertEqual(len(ope_line), 0,
                         "Operation line cost with amount 0 found.")
        self.assertFalse(
            self.mrp_repair._catch_repair_line_information_for_analytic(
                self.mrp_repair.operations[:1]))


class TestMrpRepairEstimatedCost(TestMrpRepairAnalytic):

    def setUp(self):
        super(TestMrpRepairEstimatedCost, self).setUp()

    def test_mrp_repair_create_estimated_costs_confirm(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        ope_line = self.analytic_line_model.search(
            [('account_id', '=', self.analytic_id.id),
             ('product_id', '=', self.op_product.id),
             ('is_repair_cost', '=', True),
             ('amount', '=', 0),
             ('repair_estim_amount', '=', self.op_amount)])
        fee_line = self.analytic_line_model.search(
            [('account_id', '=', self.analytic_id.id),
             ('product_id', '=', self.fee_product.id),
             ('is_repair_cost', '=', True),
             ('amount', '=', 0),
             ('repair_estim_amount', '=', self.fee_amount)])
        self.assertNotEqual(len(ope_line), 0,
                            "Operation line estimated cost not found.")
        self.assertNotEqual(len(fee_line), 0,
                            "Fee line estimated cost not found.")

    def test_exists_analytic_line_for_product(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        categ = self.op_product.categ_id
        general_account = (self.op_product.property_account_income or
                           categ.property_account_income_categ or False)
        analytic_line_vals = {
            'product_id': self.op_product.id,
            'is_repair_cost': False,
            'amount': 230,
            'unit_amount': 20,
            'account_id': self.analytic_id.id,
            'name': 'Analytic line',
            'general_account_id': general_account.id
            }
        self.analytic_line_model.create(analytic_line_vals)
        self.assertFalse(
            self.mrp_repair._catch_repair_line_information_for_analytic(
                self.mrp_repair.operations[:1]))
        self.assertFalse(
            not self.mrp_repair._catch_repair_line_information_for_analytic(
                self.mrp_repair.fees_lines[:1]))

    def test_real_cost_lines(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        self.mrp_repair.create_repair_cost()
        self.assertEqual(len(self.mrp_repair.repair_real_lines), 2,
                         "There quantity of real lines is not correct.")
        for line in self.mrp_repair.repair_real_lines:
            self.assertNotEqual(line.amount, 0,
                                "Wrong real cost line amount.")

    def test_estimated_cost_lines(self):
        self.mrp_repair.signal_workflow('repair_confirm')
        self.assertEqual(len(self.mrp_repair.repair_estim_lines), 2,
                         "There quantity of estimated lines is not correct.")
        for line in self.mrp_repair.repair_estim_lines:
            self.assertNotEqual(line.repair_estim_amount, 0,
                                "Wrong estimated cost line amount.")
