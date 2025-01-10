# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models
from odoo.osv import expression


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    def name_get(self):
        result = []
        for suppinfo in self:
            base_result = super(ProductSupplierinfo, suppinfo).name_get()
            for suppinfo_id, name in base_result:
                if self.env.context.get("show_customer_product_code"):
                    names = []
                    code = (
                        suppinfo.product_code
                        or suppinfo.product_tmpl_id.default_code
                        or False
                    )
                    if code:
                        names.append(f"[{code}]")
                    names.append(suppinfo.product_name or suppinfo.product_tmpl_id.name)
                    if names:
                        name = " ".join(names)
                result.append((suppinfo_id, name))
        return result

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        if args is None:
            args = []
        results = super()._name_search(
            name, args, operator, limit, name_get_uid=name_get_uid
        )
        products = self.env["product.product"].search([("name", operator, name)])
        domain = [
            "|",
            ("product_code", operator, name),
            ("product_name", operator, name),
        ]
        if products:
            args = expression.OR(
                [
                    domain,
                    [("product_tmpl_id", "in", products.mapped("product_tmpl_id").ids)],
                ]
            )
        else:
            args += domain
        more_results = self.search(args, limit=limit)
        return more_results.name_get() or results
