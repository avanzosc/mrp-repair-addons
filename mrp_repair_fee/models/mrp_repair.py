# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models, _
import openerp.addons.decimal_precision as dp


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    product_id = fields.Many2one(states={'draft': [('readonly', False)],
                                         'confirmed': [('readonly', False)]})
    fees_lines_to_invoice = fields.One2many(
        comodel_name='mrp.repair.fee', inverse_name='repair_id',
        string='Fees to invoice', copy=True,
        readonly=True, states={'draft': [('readonly', False)]},
        domain=[('to_invoice', '=', True)])
    fees_lines_no_to_invoice = fields.One2many(
        comodel_name='mrp.repair.fee', inverse_name='repair_id',
        string='Fees to NOT invoice', copy=True,
        readonly=True, states={'draft': [('readonly', False)]},
        domain=[('to_invoice', '=', False)])


class MrpRepairFee(models.Model):
    _inherit = 'mrp.repair.fee'

    @api.multi
    def _catch_default_to_invoice(self):
        return self.env.context.get('to_invoice', True)

    @api.multi
    @api.depends('product_id', 'product_uom_qty')
    def _compute_cost_subtotal(self):
        for fee in self:
            fee.standard_price = fee.product_id.standard_price
            fee.cost_subtotal = (fee.product_id.standard_price *
                                 fee.product_uom_qty)

    imputation_date = fields.Date(string='Imputation Date')
    to_invoice = fields.Boolean(default=_catch_default_to_invoice)
    standard_price = fields.Float(
        string='Cost Price', digits_compute=dp.get_precision('Account'),
        compute='_compute_cost_subtotal', store=True)
    cost_subtotal = fields.Float(
        string='Cost Subtotal', digits_compute=dp.get_precision('Account'),
        compute='_compute_cost_subtotal', store=True)
    repair_pricelist = fields.Many2one(
        related='repair_id.pricelist_id', string='Pricelist')
    repair_partner = fields.Many2one(
        related='repair_id.partner_id', string='Partner', store=True)
    repair_product = fields.Many2one(
        related='repair_id.product_id', string='Product To Repair',
        store=True)
    repair_lot = fields.Many2one(
        related='repair_id.lot_id', string='Repair Lot', store=True)
    repair_guarantee_limit = fields.Date(
        related='repair_id.guarantee_limit', string='Warranty Expiration')

    @api.onchange('user_id')
    def _onchange_user_id(self):
        employee_obj = self.env['hr.employee']
        result = {}
        cond = [('user_id', '=', self.user_id.id)]
        employee = employee_obj.search(cond, limit=1)
        if employee and employee.product_id:
            self.product_id = employee.product_id.id
        else:
            warning = {'title': _('Warning!')}
            if not employee:
                warning['message'] = _('User does not have any employee '
                                       'assigned')
                self.name = _('Associate employee to user')
            elif not employee.product_id:
                warning['message'] = _('The employee associated with the user'
                                       ' has not defined any product')
                self.name = _('Associate product to employee')
            self.product_id = False
            result['warning'] = warning
        return result

    @api.multi
    @api.onchange('repair_id')
    def onchange_repair_id(self):
        self.ensure_one()
        res = {}
        if self.repair_id:
            res = self.product_id_change(
                self.repair_id.pricelist_id.id, self.product_id.id,
                uom=self.product_uom.id, product_uom_qty=self.product_uom_qty,
                partner_id=self.repair_id.partner_id.id,
                guarantee_limit=self.repair_id.guarantee_limit)
        return res

    def product_id_change(
            self, cr, uid, ids, pricelist, product, uom=False,
            product_uom_qty=0, partner_id=False, guarantee_limit=False,
            context=None):
        if not pricelist:
            pricelist = self.pool['product.pricelist'].search(
                cr, uid, [('type', '=', 'sale')], limit=1, context=context)[0]
        res = super(MrpRepairFee, self).product_id_change(
            cr, uid, ids, pricelist, product, uom=uom,
            product_uom_qty=product_uom_qty, partner_id=partner_id,
            guarantee_limit=guarantee_limit, context=context)
        return res


class MrpRepairLine(models.Model):
    _inherit = 'mrp.repair.line'

    @api.depends('product_id', 'product_uom_qty')
    def _compute_cost_subtotal(self):
        for line in self:
            line.standard_price = line.product_id.standard_price
            line.cost_subtotal = (line.product_id.standard_price *
                                  line.product_uom_qty)

    standard_price = fields.Float(
        string='Cost Price', digits_compute=dp.get_precision('Account'),
        compute='_compute_cost_subtotal', store=True)
    cost_subtotal = fields.Float(
        string='Cost Subtotal', digits_compute=dp.get_precision('Account'),
        compute='_compute_cost_subtotal', store=True)
