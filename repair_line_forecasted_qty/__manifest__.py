# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Repair Line Forecasted Qty",
    "version": "14.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "depends": ["repair", "stock", "web"],
    "data": [
        "views/repair_order_views.xml",
        "report/report_stock_forecasted.xml",
    ],
    "qweb": ["static/src/xml/repair_line_forecasted_qty.xml"],
    "installable": True,
}
