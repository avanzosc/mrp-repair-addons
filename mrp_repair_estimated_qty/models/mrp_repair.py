# -*- coding: utf-8 -*-
# (c) 2015 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class MrpRepairLine(models.Model):

    _inherit = 'mrp.repair.line'

    @api.multi
    @api.depends('product_id', 'product_uom_qty', 'lot_id', 'expected_qty')
    def _compute_cost_subtotal(self):
        super(MrpRepairLine, self)._compute_cost_subtotal()
        for line in self:
            qty = line.expected_qty or line.product_uom_qty
            line.cost_subtotal = line.standard_price * qty

    @api.multi
    @api.depends('expected_qty', 'product_uom_qty', 'price_unit', 'product_id',
                 'tax_id', 'repair_id.partner_id',
                 'repair_id.pricelist_id.currency_id')
    def _get_line_subtotal(self):
        for line in self:
            qty = line.expected_qty or line.product_uom_qty
            taxes = line.tax_id.compute_all(
                line.price_unit, qty, line.product_id,
                line.repair_id.partner_id)
            cur = line.repair_id.pricelist_id.currency_id
            subtotal = cur.round(taxes['total'])
            line.price_subtotal = subtotal

    expected_qty = fields.Float(string='Expected Qty',
                                digits=dp.get_precision(
                                    'Product Unit of Measure'))
    product_uom_qty = fields.Float(string='Real Qty', default=0)
    price_subtotal = fields.Float(compute='_get_line_subtotal')

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
        if product_uom_qty == 0:
            res['value']['product_uom_qty'] = 0
        return res


class MrpRepair(models.Model):

    _inherit = 'mrp.repair'

    def _catch_repair_line_information_for_analytic(self, line):
        res = super(MrpRepair,
                    self)._catch_repair_line_information_for_analytic(line)
        ctx = self.env.context
        if (not line._name == 'mrp.repair.line' or not line.expected_qty or not
                ctx.get('load_estimated', False)):
            return res
        if res:
            res['unit_amount'] = line.expected_qty
            res['repair_estim_amount'] = (line.product_id.standard_price *
                                          line.expected_qty * -1)
            res['amount'] = 0
        else:
            analytic_line_obj = self.env['account.analytic.line']
            journal = self.env.ref('mrp.analytic_journal_repair', False)
            name = self.name
            if line.product_id.default_code:
                name += ' - ' + line.product_id.default_code
            categ_id = line.product_id.categ_id
            general_account = (line.product_id.property_account_income or
                               categ_id.property_account_income_categ or False)
            amount = line.product_id.standard_price * line.expected_qty * -1
            res = {
                'name': name,
                'user_id': line.user_id.id,
                'date': analytic_line_obj._get_default_date(),
                'product_id': line.product_id.id,
                'unit_amount': line.expected_qty,
                'product_uom_id': line.product_uom.id,
                'amount': 0,
                'repair_estim_amount': amount,
                'journal_id': journal.id,
                'account_id': self.analytic_account.id,
                'is_repair_cost': True,
                'general_account_id': general_account.id
                }
        return res
