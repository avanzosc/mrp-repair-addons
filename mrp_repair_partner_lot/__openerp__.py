# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "MRP Repair Partner Lot",
    "version": "8.0.1.1.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Manufacturing",
    "depends": [
        "stock",
        "mrp_repair",
        "product_supplierinfo_for_customer",
        "mrp_calendar_view"
    ],
    "data": [
        "security/ir.model.access.csv",
        "report/mrp_repair_report.xml",
        "data/report_paperformat.xml",
        "views/mrp_repair_view.xml",
        "views/mrp_repair_customer_lot_view.xml",
    ],
    "installable": True,
}
