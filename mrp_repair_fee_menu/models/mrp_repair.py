# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    fees_lines_to_invoice = fields.One2many(
        'mrp.repair.fee', 'repair_id', string='Fees to invoice',
        readonly=True, states={'draft': [('readonly', False)]}, copy=True,
        domain=[('to_invoice', '=', True)])
    fees_lines_no_to_invoice = fields.One2many(
        'mrp.repair.fee', 'repair_id', string='Fees to NOT invoice',
        readonly=True, states={'draft': [('readonly', False)]}, copy=True,
        domain=[('to_invoice', '=', False)])


class MrpRepairFee(models.Model):
    _inherit = 'mrp.repair.fee'

    to_invoice = fields.Boolean(default=False)
    standard_price = fields.Float(
        string='Cost Price', related='product_id.standard_price')
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

    @api.multi
    @api.onchange('user_id')
    def _onchange_user_id(self):
        employee_obj = self.env['hr.employee']
        self.ensure_one()
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
            elif not employee.product_id:
                warning['message'] = _('The employee associated with the user'
                                       ' has not defined any product')
            self.product_id = False
            self.name = False
            result['warning'] = warning
        return result
