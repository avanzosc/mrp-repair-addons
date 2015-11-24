# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín <esthermartin@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Mrp Repair Expense",
    "version": "8.0.1.0.0",
    'author': 'AvanzOSC',
    'website': "http://www.avanzosc.es",
    'contributors': [
        "Ana Juaristi <ajuaristio@gmail.com>",
        "Esther Martín <esthermartin@avanzosc.es>"
    ],
    "depends": [
        "mrp_repair",
        "hr_expense",
        "mrp_repair_analytic",
    ],
    "category": "Manufacturing",
    "data": [
        "views/mrp_repair_view.xml",
        "views/hr_expense_view.xml",
    ],
    "installable": True
}
