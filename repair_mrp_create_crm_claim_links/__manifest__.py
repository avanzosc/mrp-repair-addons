# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Repair MRP Create Crm Claim Links",
    "summary": "Create manufacturing orders from repair orders.",
    "version": "18.0.1.0.0",
    "category": "Manufacturing/Manufacturing",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "author": "AvanzOSC",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "repair_mrp_create",
        "crm_claim_links",
    ],
    "data": [
        "views/mrp_production_views.xml",
        "views/crm_claim_views.xml",
    ],
    "auto_install": True,
}
