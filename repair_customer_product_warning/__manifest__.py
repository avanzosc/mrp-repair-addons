# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Repair Customer Product Warning",
    "version": "16.0.1.0.0",
    "category": "Inventory/Inventory",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "depends": [
        "repair",
        "account_invoice_section_repair",
    ],
    "data": [
        "security/res_groups.xml",
        "views/res_config_settings_view.xml",
        "views/res_partner_view.xml",
        "views/product_views.xml",
    ],
    "installable": True,
}
