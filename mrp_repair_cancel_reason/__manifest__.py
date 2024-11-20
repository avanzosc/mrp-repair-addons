# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Repair Cancel Reason",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "category": "Inventory/Inventory",
    "depends": [
        "repair",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/repair_order_cancel_reason.xml",
        "wizard/wiz_repair_order_cancel_reason_view.xml",
        "views/repair_order_view.xml",
        "views/repair_order_cancel_reason_view.xml",
    ],
    "installable": True,
}
