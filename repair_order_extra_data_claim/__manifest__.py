# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Repair Order Extra Data Claim",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "https://github.com/avanzosc/mrp-repair-addons",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Inventory/Inventory",
    "depends": ["repair_order_extra_data", "crm_claim_links"],
    "data": [
        "report/mrp_repair_report.xml",
    ],
    "installable": True,
    "auto_install": True,
}
