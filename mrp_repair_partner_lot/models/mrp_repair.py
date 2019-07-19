# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    customer_lot_ids = fields.One2many(
        comodel_name='mrp.repair.customer.lot',
        inverse_name='repair_id', string='Customer lots')


class MrpRepairCustomerLot(models.Model):
    _name = 'mrp.repair.customer.lot'
    _description = "MRP repair customer lot"

    repair_id = fields.Many2one(
        comodel_name='mrp.repair', string='Repair order')
    repair_date = fields.Date(
        string='Repair date', compute='_compute_repair_date',
        store=True)
    customer_id = fields.Many2one(
        comodel_name='res.partner', string='Customer',
        related='repair_id.partner_id', store=True)
    product_code = fields.Many2one(
        string='Customer product code', comodel_name='product.supplierinfo')
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template', string='Product template',
        related='product_code.product_tmpl_id', store=True)
    lot_id = fields.Many2one(
        comodel_name='stock.production.lot', string='Lot')
    quantity = fields.Float(
        string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    description_breakdown = fields.Text(string='Description breakdown')
    cause = fields.Text(string='Cause')
    repair_made = fields.Text(string='Repair made')
    repairable = fields.Boolean(string='Repairable')

    @api.depends('repair_id', 'repair_id.date_repair')
    def _compute_repair_date(self):
        for lot in self.filtered(lambda l: l.repair_id and
                                 l.repair_id.date_repair):
            lot.repair_date = (
                fields.Datetime.from_string(lot.repair_id.date_repair).date())
