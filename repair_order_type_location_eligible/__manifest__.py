# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Repair Order Type Location Eligible",
    "summary": "",
    "version": "16.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "depends": [
        "repair_type",
        "repair_order_location_eligible",
    ],
    "data": ["views/repair_order_type_views.xml"],
    "installable": True,
    "auto_install": True,
}
