# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'MRP Repair Date',
    "version": "8.0.1.0.0",
    "license": 'AGPL-3',
    "author": 'OdooMRP team,'
              'AvanzOSC,'
              'Serv. Tecnol. Avanzados - Pedro M. Baeza',
    'website': "http://www.odoomrp.com",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
        ],
    'category': 'Manufacturing',
    'depends': ['mrp_repair',
                ],
    'data': ['views/mrp_repair_view.xml',
             ],
    'installable': True,
}
