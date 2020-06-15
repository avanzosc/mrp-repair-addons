# -*- coding: utf-8 -*-
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mrp Repair Kanban",
    "version": "8.0.1.0.1",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Daniel Campos <danielcampos@avanzosc.es>",
    ],
    "depends": ["hr", "mrp", "mrp_repair", "mrp_repair_fee"],
    "data": [
        "views/hr_employee_view.xml",
        "views/mrp_repair_view.xml",
        "views/mrp_repair_fee_view.xml",
        "views/users_view.xml",
        "security/ir.model.access.csv",
        "wizard/wizard_repair_fee_view.xml",
    ],
    "installable": True,
}
