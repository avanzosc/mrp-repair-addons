from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    customer_lot_ids = fields.One2many(
        comodel_name="repair.order.customer.lot",
        inverse_name="repair_id",
        string="Customer lots",
    )


class MrpRepairCustomerLot(models.Model):
    _name = "repair.order.customer.lot"
    _description = "MRP Repair Customer Lot"

    repair_id = fields.Many2one(comodel_name="repair.order", required=True)
    date_repair = fields.Datetime(related="repair_id.date_repair", store=True)
    customer_id = fields.Many2one(
        comodel_name="res.partner",
        related="repair_id.partner_id",
        store=True,
    )
    customer_product_code = fields.Char()
    lot_id = fields.Many2one(comodel_name="stock.production.lot", required=True)
    product_variant_id = fields.Many2one(comodel_name="product.product", required=True)
    product_template_id = fields.Many2one(
        comodel_name="product.template",
        related="product_variant_id.product_tmpl_id",
        store=True,
    )
    internal_reference = fields.Char(
        related="product_variant_id.default_code",
        store=True,
    )
    quantity = fields.Integer()
    breakdown_description = fields.Text()
    cause = fields.Text()
    repair_made = fields.Text()
    repairable = fields.Boolean()

    @api.onchange("lot_id")
    def _onchange_lot_id(self):
        """Set the product variant when a lot is selected."""
        for record in self:
            record.product_variant_id = record.lot_id.product_id
