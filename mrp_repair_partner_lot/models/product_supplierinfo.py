# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.multi
    def name_get(self):
        if 'show_customer_product_code' in self.env.context:
            new_res = []
            for product in self:
                name = u"[{}] {}".format(
                    product.product_code or '', product.product_name or '')
                new_res.append((product.id, name))
            return new_res
        else:
            return super(ProductSupplierinfo, self).name_get()
