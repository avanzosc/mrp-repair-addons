# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    'name': 'MRP Repair Cancel Reason',
    "version": "16.0.1.0.0",
    "license": 'AGPL-3',
    "author": 'AvanzOSC',
    'website': "http://www.odoomrp.com",
    "contributors": [
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
        ],
    'category': 'Manufacturing',
    'depends': ['product',
                'stock',
                'mrp',
                ],
    'data': ['security/ir.model.access.csv',
             'data/repair_order_cancel_reason.xml',
             'wizard/wiz_repair_order_cancel_reason_view.xml',
             'views/repair_order_view.xml',
             'views/repair_order_cancel_reason_view.xml',
             ],
    'installable': True,
}
