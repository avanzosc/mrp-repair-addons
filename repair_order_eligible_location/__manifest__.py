# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Repair Order Eligible Location",
    "summary": "",
    "version": "16.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "depends": [
        "repair",
        "stock",
    ],
    "data": ["views/stock_location_views.xml", "views/repair_order_views.xml"],
    "installable": True,
}
