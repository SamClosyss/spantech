# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Inventory Force Date',
    "summary": """
  Inventory Force Date
  """,
    'description': """
   Inventory Force Date
""",
    # 'version': '14.0.0.1',
    'category': 'stock',
    'license': 'LGPL-3',
    'sequence': 1,
    'author': "Eng-Mahmoud Ramadan",
    'website': 'mramadan271193@gmail.com',
    'depends': [
        'base',
        'stock',
    ],

    'data': [
        'security/group.xml',
        'views/stock_quant.xml',
        'views/stock_picking.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
    'price': 20,
    'currency': 'EUR',
}
