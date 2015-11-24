# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín <esthermartin@avanzosc.es> - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Mrp Repair Expense",
    "version": "8.0.1.0.0",
    'author': 'OdooMRP team',
    'website': "http://www.odoomrp.com",
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
        "views/mrp_repair.xml",
        "views/hr_expense.xml",
    ],
    "installable": True
}
