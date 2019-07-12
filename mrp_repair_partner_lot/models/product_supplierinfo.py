# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, models
from openerp.models import expression


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.multi
    def name_get(self):
        results = []
        for suppinfo in self:
            result = super(ProductSupplierinfo, suppinfo).name_get()
            for suppinfo_id, name in result:
                if self.env.context.get('show_customer_product_code'):
                    names = []
                    code = (suppinfo.product_code or
                            suppinfo.product_tmpl_id.default_code or False)
                    if code:
                        names.append('[{}]'.format(code))
                    names.append(suppinfo.product_name or
                                 suppinfo.product_tmpl_id.name)
                    if names:
                        name = ' '.join(names)
                suppinfo_name = [suppinfo_id, name]
                results.append(tuple(suppinfo_name))
        return results

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        results = super(ProductSupplierinfo,
                        self).name_search(name, args, operator, limit)
        products = self.env['product.product'].search(
            [('name', operator, name)])
        domain = ['|', ('product_code', operator, name),
                  ('product_name', operator, name)]
        if products:
            args += expression.OR([domain,
                                   [('product_tmpl_id', 'in', products.mapped(
                                     'product_tmpl_id').ids)]])
        else:
            args += domain
        more_results = self.search(args)
        return more_results and more_results.name_get() or results
