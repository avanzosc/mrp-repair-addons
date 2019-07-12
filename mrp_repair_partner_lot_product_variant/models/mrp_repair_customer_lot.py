# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class MrpRepairCustomerLot(models.Model):
    _inherit = 'mrp.repair.customer.lot'

    product_id = fields.Many2one(
        comodel_name='product.product', string='Product variant',
        related='product_code.product_id', store=True)
