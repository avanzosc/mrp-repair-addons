# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Repair MRP Create",
    "summary": "Create manufacturing orders from repair orders.",
    "version": "18.0.1.0.0",
    "category": "Manufacturing/Manufacturing",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "author": "AvanzOSC, Odoo Community Association (OCA)",
    "maintainers": ["aneravanzosc"],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "repair",
        "mrp",
    ],
    "data": [
        "views/mrp_bom_views.xml",
        "views/repair_order_views.xml",
        "views/mrp_production_views.xml",
        "views/mrp_workorder_views.xml",
    ],
}
