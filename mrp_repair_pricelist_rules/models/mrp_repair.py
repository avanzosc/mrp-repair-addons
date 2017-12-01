# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, _
from openerp.osv import fields as old_fields
import openerp.addons.decimal_precision as dp


class MrpRepairLine(models.Model):
    _inherit = 'mrp.repair.line'

    @api.multi
    def _amount_line(self, field_name, arg):
        res = super(MrpRepairLine, self)._amount_line(field_name, arg)
        for line in self.filtered(lambda l: l.discount or l.discount2 or
                                  l.discount3):
            try:
                qty = line.expected_qty or line.product_uom_qty
            except Exception:
                qty = line.product_uom_qty
            price = (line.price_unit *
                     (1 - (line.discount or 0.0) / 100) *
                     (1 - (line.discount2 or 0.0) / 100) *
                     (1 - (line.discount3 or 0.0) / 100))
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

    @api.multi
    def _get_possible_item_ids(self, pricelist_id, product_id=False, qty=0):
        item_obj = self.env['product.pricelist.item']
        item_ids = item_obj.domain_by_pricelist(
            pricelist_id, product_id=product_id, qty=qty)
        return item_ids

    @api.multi
    @api.depends('product_id', 'product_uom_qty',
                 'repair_id.pricelist_id')
    def _compute_possible_items(self):
        for record in self:
            item_ids = record._get_possible_item_ids(
                record.repair_id.pricelist_id.id,
                product_id=record.product_id.id,
                qty=record.product_uom_qty)
            record.possible_item_ids = [(6, 0, item_ids)]

    discount = fields.Float(
        string='Disc. (%)', digits=dp.get_precision('Discount'), default=0.0)
    discount2 = fields.Float(
        string='Disc. 2 (%)', digits=dp.get_precision('Discount'), default=0.0)
    discount3 = fields.Float(
        string='Disc. 3 (%)', digits=dp.get_precision('Discount'), default=0.0)
    item_id = fields.Many2one(
        comodel_name='product.pricelist.item', string='Pricelist Item')
    possible_item_ids = fields.Many2many(
        comodel_name='product.pricelist.item',
        compute='_compute_possible_items')

    _sql_constraints = [
        ('discount_limit', 'CHECK (discount <= 100.0)',
         _('The discount must be lower than 100%.')),
        ('discount2_limit', 'CHECK (discount2 <= 100.0)',
         _('Second discount must be lower than 100%.')),
        ('discount3_limit', 'CHECK (discount3 <= 100.0)',
         _('Third discount must be lower than 100%.')),
    ]

    def default_get(self, cr, uid, fields_list, context=None):
        res = super(MrpRepairLine, self).default_get(cr, uid, fields_list,
                                                     context=context)
        item_obj = self.pool['product.pricelist.item']
        if context.get('pricelist_id'):
            item_id = item_obj.get_best_pricelist_item(
                cr, uid, context['pricelist_id'], context=context)
            res.update({'item_id': item_id})
        return res

    def product_id_change(self, cr, uid, ids, pricelist, product, uom=False,
                          product_uom_qty=0, partner_id=False,
                          guarantee_limit=False, context=None):
        res = super(MrpRepairLine, self).product_id_change(
            cr, uid, ids, pricelist, product, uom=uom,
            product_uom_qty=product_uom_qty, partner_id=partner_id,
            guarantee_limit=guarantee_limit, context=context)
        if 'domain' not in res:
            res['domain'] = {}
        warning_msgs = res.get('warning') and res['warning']['message'] or ''
        item_obj = self.pool['product.pricelist.item']
        if product:
            item_id = item_obj.get_best_pricelist_item(
                cr, uid, pricelist, product_id=product, qty=product_uom_qty,
                partner_id=partner_id, context=context)
            if not item_id:
                warn_msg = _('Cannot find a pricelist line matching this '
                             'product and quantity.\nYou have to change either'
                             ' the product, the quantity or the pricelist.')
                warning_msgs += (_("No valid pricelist line found ! :") +
                                 warn_msg + "\n\n")
            else:
                res['value']['price_unit'] = item_obj.browse(
                    cr, uid, item_id, context=context).price_get(
                        product, product_uom_qty, partner_id, uom)[0]
                res['value'].update({'item_id': item_id})
                line_obj = self.pool['mrp.repair.line'].browse(
                    cr, uid, ids, context=context)
                res['domain'].update(
                    {'item_id': [('id', 'in', line_obj._get_possible_item_ids(
                        pricelist, product_id=product, qty=product_uom_qty))]})
        if warning_msgs:
            res['warning'] = {'title': _('Configuration Error!'),
                              'message': warning_msgs}
        return res

    @api.multi
    @api.onchange('item_id')
    def onchange_item_id(self):
        self.ensure_one()
        if self.item_id:
            self.discount = self.item_id.discount
            self.discount2 = self.item_id.discount2
            self.discount3 = self.item_id.discount3
            if self.product_id:
                self.price_unit = self.item_id.price_get(
                    self.product_id.id, self.product_uom_qty,
                    self.repair_id.partner_id.id, self.product_id.uom_id.id)[0]


class MrpRepairFee(models.Model):
    _inherit = 'mrp.repair.fee'

    @api.multi
    @api.depends('product_uom_qty', 'price_unit', 'product_id',
                 'tax_id', 'repair_id.partner_id', 'to_invoice', 'discount3',
                 'repair_id.pricelist_id.currency_id', 'discount', 'discount2')
    def _compute_line_subtotal(self):
        for line in self:
            qty = line.product_uom_qty
            price = (line.price_unit *
                     (1 - (line.discount or 0.0) / 100) *
                     (1 - (line.discount2 or 0.0) / 100) *
                     (1 - (line.discount3 or 0.0) / 100))
            taxes = line.tax_id.compute_all(
                price, qty, line.product_id, line.repair_id.partner_id)
            cur = line.repair_id.pricelist_id.currency_id
            subtotal = cur.round(taxes['total'])
            line.price_subtotal = subtotal

    @api.multi
    def _get_possible_item_ids(self, pricelist_id, product_id=False, qty=0):
        item_obj = self.env['product.pricelist.item']
        item_ids = item_obj.domain_by_pricelist(
            pricelist_id, product_id=product_id, qty=qty)
        return item_ids

    @api.multi
    @api.depends('product_id', 'product_uom_qty',
                 'repair_id.pricelist_id')
    def _compute_possible_items(self):
        for record in self:
            item_ids = record._get_possible_item_ids(
                record.repair_id.pricelist_id.id,
                product_id=record.product_id.id,
                qty=record.product_uom_qty)
            record.possible_item_ids = [(6, 0, item_ids)]

    discount = fields.Float(
        string='Disc. (%)', digits=dp.get_precision('Discount'), default=0.0)
    discount2 = fields.Float(
        string='Disc. 2 (%)', digits=dp.get_precision('Discount'), default=0.0)
    discount3 = fields.Float(
        string='Disc. 3 (%)', digits=dp.get_precision('Discount'), default=0.0)
    item_id = fields.Many2one(
        comodel_name='product.pricelist.item', string='Pricelist Item')
    price_subtotal = fields.Float(compute='_compute_line_subtotal')
    possible_item_ids = fields.Many2many(
        comodel_name='product.pricelist.item',
        compute='_compute_possible_items')

    _sql_constraints = [
        ('discount_limit', 'CHECK (discount <= 100.0)',
         _('The discount must be lower than 100%.')),
        ('discount2_limit', 'CHECK (discount2 <= 100.0)',
         _('Second discount must be lower than 100%.')),
        ('discount3_limit', 'CHECK (discount3 <= 100.0)',
         _('Third discount must be lower than 100%.')),
    ]

    def default_get(self, cr, uid, fields_list, context=None):
        res = super(MrpRepairFee, self).default_get(cr, uid, fields_list,
                                                    context=context)
        item_obj = self.pool['product.pricelist.item']
        if context.get('pricelist_id'):
            item_id = item_obj.get_best_pricelist_item(
                cr, uid, context['pricelist_id'], context=context)
            self.onchange_item_id()
            res.update({'item_id': item_id})
        return res

    def product_id_change(self, cr, uid, ids, pricelist, product, uom=False,
                          product_uom_qty=0, partner_id=False,
                          guarantee_limit=False, context=None):
        res = super(MrpRepairFee, self).product_id_change(
            cr, uid, ids, pricelist, product, uom=uom,
            product_uom_qty=product_uom_qty, partner_id=partner_id,
            guarantee_limit=guarantee_limit, context=context)
        if 'domain' not in res:
            res['domain'] = {}
        warning_msgs = res.get('warning') and res['warning']['message'] or ''
        item_obj = self.pool['product.pricelist.item']
        if product:
            item_id = item_obj.get_best_pricelist_item(
                cr, uid, pricelist, product_id=product, qty=product_uom_qty,
                partner_id=partner_id, context=context)
            if not item_id:
                warn_msg = _('Cannot find a pricelist line matching this '
                             'product and quantity.\nYou have to change either'
                             ' the product, the quantity or the pricelist.')
                warning_msgs += (_("No valid pricelist line found ! :") +
                                 warn_msg + "\n\n")
            else:
                res['value']['price_unit'] = item_obj.browse(
                    cr, uid, item_id, context=context).price_get(
                    product, product_uom_qty, partner_id, uom)[0]
                res['value'].update({'item_id': item_id})
                fee_obj = self.pool['mrp.repair.fee'].browse(
                    cr, uid, ids, context=context)
                res['domain'].update(
                    {'item_id': [('id', 'in', fee_obj._get_possible_item_ids(
                        pricelist, product_id=product, qty=product_uom_qty))]})
        if warning_msgs:
            res['warning'] = {'title': _('Configuration Error!'),
                              'message': warning_msgs}
        return res

    @api.multi
    @api.onchange('item_id')
    def onchange_item_id(self):
        self.ensure_one()
        if self.item_id:
            self.discount = self.item_id.discount
            self.discount2 = self.item_id.discount2
            self.discount3 = self.item_id.discount3
            if self.product_id:
                self.price_unit = self.item_id.price_get(
                    self.product_id.id, self.product_uom_qty,
                    self.repair_id.partner_id.id, self.product_id.uom_id.id)[0]


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    @api.multi
    @api.onchange('pricelist_id')
    def onchange_pricelist_id(self):
        self.ensure_one()
        if self.pricelist_id:
            item_obj = self.env['product.pricelist.item']
            for line in self.fees_lines:
                line.item_id = item_obj.get_best_pricelist_item(
                    self.pricelist_id.id, product_id=line.product_id.id,
                    qty=line.product_uom_qty,
                    partner_id=line.repair_id.partner_id.id)
                line.onchange_item_id()
            for line in self.operations:
                line.item_id = item_obj.get_best_pricelist_item(
                    self.pricelist_id.id, product_id=line.product_id.id,
                    qty=line.product_uom_qty,
                    partner_id=line.repair_id.partner_id.id)
                line.onchange_item_id()

    @api.multi
    def action_invoice_create(self, group=False):
        res = super(MrpRepair, self).action_invoice_create(group=group)
        for repair_id in res:
            repair = self.browse(repair_id)
            for line in repair.fees_lines.filtered(lambda x: x.to_invoice):
                disc = ((1 - ((1 - line.discount / 100) *
                              (1 - line.discount2 / 100) *
                              (1 - line.discount3 / 100))) * 100)
                line.invoice_line_id.discount = disc
            for line in repair.operations.filtered(lambda x: x.to_invoice):
                disc = ((1 - ((1 - line.discount / 100) *
                              (1 - line.discount2 / 100) *
                              (1 - line.discount3 / 100))) * 100)
                line.invoice_line_id.discount = disc
        return res
