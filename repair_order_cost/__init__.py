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
            operation.onchange_product_id()
        for line in repair.fees_lines:
            line.onchange_product_id()
