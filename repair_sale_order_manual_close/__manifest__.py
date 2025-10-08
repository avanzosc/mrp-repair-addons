# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Repair To Sale Order - Manual Close",
    "version": "14.0.1.0.0",
    "category": "Repair",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "depends": [
        "repair_sale_order",
    ],
    "data": [
        "data/repair_sale_order_manual_close_data.xml",
        "views/repair_order_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
