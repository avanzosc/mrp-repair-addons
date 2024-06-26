from . import models
from odoo import api, SUPERUSER_ID


def _post_install_put_cost_in_repair_orders(cr, registry):
    """
    This method will set the production cost on already done manufacturing orders.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    repairs = env["repair.order"].search([])
    for repair in repairs:
        for operation in repair.operations:
            operation.material_cost = (
                operation.product_uom_qty * operation.product_id.standard_price
            )
        for line in repair.fees_lines:
            line.operations_cost = line.product_uom_qty * line.product_id.standard_price
