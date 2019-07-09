# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.multi
    def name_get(self):
        if self.env.context.get('show_customer_product_code', False):
            new_res = []
            for product in self.filtered(
                    lambda x: x.product_code or x.product_name):
                name = u"[{}] {}".format(
                    product.product_code or '', product.product_name or '')
                new_res.append((product.id, name))
            if new_res:
                return new_res
        return super(ProductSupplierinfo, self).name_get()
