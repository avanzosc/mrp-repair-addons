from . import models


def _post_install_put_cost_in_repair_orders(env):
    """
    This method will set the production cost on already done manufacturing orders.
    """
    repair_services = env["repair.service"].search([])
    for repair_service in repair_services:
        repair_service.operations_cost = (
            repair_service.product_uom_qty * repair_service.product_id.standard_price
        )
