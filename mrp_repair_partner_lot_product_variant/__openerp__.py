# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "MRP Repair Partner Lot Product Variant",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Manufacturing",
    "depends": [
        "mrp_repair_partner_lot",
        "product_variant_supplierinfo",
    ],
    "data": [
        "report/mrp_repair_report.xml",
        "views/mrp_repair_customer_lot_view.xml",
        "views/mrp_repair_view.xml",
    ],
    "installable": True,
    "autoinstall": True,
}
