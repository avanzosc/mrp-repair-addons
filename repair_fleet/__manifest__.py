# Copyright 2025 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Fleet Repair",
    "version": "14.0.1.0.0",
    "category": "Repair",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "license": "LGPL-3",
    "depends": [
        "repair",
        "fleet",
        "product",
    ],
    "data": ["views/product_category_views.xml", "views/repair_order_views.xml"],
    "installable": True,
    "application": False,
}
