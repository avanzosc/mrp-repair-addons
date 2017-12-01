# -*- coding: utf-8 -*-
# Copyright 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.osv import fields as old_fields
from openerp.addons import decimal_precision as dp


class MrpRepairLine(models.Model):
    _inherit = 'mrp.repair.line'

    @api.multi
    def _amount_line(self, field_name, arg):
        res = super(MrpRepairLine, self)._amount_line(field_name, arg)
        for line in self:
            qty = line.expected_qty or line.product_uom_qty
            try:
                price = (line.price_unit *
                         (1 - (line.discount or 0.0) / 100) *
                         (1 - (line.discount2 or 0.0) / 100) *
                         (1 - (line.discount3 or 0.0) / 100))
            except Exception:
                price = line.price_unit
            taxes = line.tax_id.compute_all(
                price, qty, line.product_id, line.repair_id.partner_id)
            cur = line.repair_id.pricelist_id.currency_id
            subtotal = cur.round(taxes['total'])
            res[line.id] = subtotal
        return res

    _columns = {
        # Must be defined in old API so that we can call super in the compute
        'price_subtotal': old_fields.function(
            _amount_line, string='Subtotal',
            digits_compute=dp.get_precision('Account')),
    }

    expected_qty = fields.Float(string='Expected Qty',
                                digits=dp.get_precision(
                                    'Product Unit of Measure'))
    repair_state = fields.Selection(related="repair_id.state")

    @api.multi
    def write(self, vals):
        res = super(MrpRepairLine, self).write(vals)
        inv_line_obj = self.env['account.invoice.line']
        for line in self:
            if vals.get('invoiced', False) and line.expected_qty and \
                    vals.get('invoice_line_id', False):
                invoice_line = inv_line_obj.browse(vals.get('invoice_line_id'))
                invoice_line.write({'quantity': self.expected_qty})
        return res

    def product_id_change(self, cr, uid, ids, pricelist, product, uom=False,
                          product_uom_qty=0, partner_id=False,
                          guarantee_limit=False, context=None):
        res = super(MrpRepairLine, self).product_id_change(
            cr, uid, ids, pricelist, product, uom=uom,
            product_uom_qty=product_uom_qty, partner_id=partner_id,
            guarantee_limit=guarantee_limit, context=context)
        if context.get('default_repair_state', False) == 'draft':
            res['value']['product_uom_qty'] = 0
            res['value']['expected_qty'] = context.get('repair_qty', 0)
        else:
            res['value']['product_uom_qty'] = context.get('repair_qty', 0)
            res['value']['expected_qty'] = 0
        return res


class MrpRepair(models.Model):

    _inherit = 'mrp.repair'

    def _catch_repair_line_information_for_analytic(self, line):
        res = super(MrpRepair,
                    self)._catch_repair_line_information_for_analytic(line)
        ctx = self.env.context
        load_estim = ctx.get('load_estimated', False)
        if line._name == 'mrp.repair.line' and load_estim and \
                not line.expected_qty:
            return False
        elif line._name == 'mrp.repair.line' and load_estim and \
                line.expected_qty:
            analytic_line_obj = self.env['account.analytic.line']
            journal = self.env.ref('mrp.analytic_journal_repair', False)
            name = self.name
            if line.product_id.default_code:
                name += ' - ' + line.product_id.default_code
            categ_id = line.product_id.categ_id
            general_account = (line.product_id.property_account_income or
                               categ_id.property_account_income_categ or False)
            res = {
                'name': name,
                'user_id': line.user_id.id,
                'date': analytic_line_obj._get_default_date(),
                'product_id': line.product_id.id,
                'unit_amount': line.expected_qty,
                'product_uom_id': line.product_uom.id,
                'amount': 0,
                'journal_id': journal.id,
                'account_id': self.analytic_account.id,
                'is_repair_cost': True,
                'general_account_id': general_account.id,
                'repair_estim_amount': (line.standard_price *
                                        line.expected_qty * -1)
            }
        return res
