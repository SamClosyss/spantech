# -*- coding: utf-8 -*-
{
    "name": "iPay Payment Acquirer",
    "license": "OPL-1",
    "summary": """
        Let your customers decide how they want to pay, from cards (debit, credit) to mobile money, to multi-currencies
        """,
    "description": """
 VISA
 Mastercard
 mVisa
 MasterPass
 M-pesa
 Lipa na Bonga
 Airtel Money
 Equitel
 Eazzypay
 eLipa

iPay Africa <https://ipayafrica.com/>
    """,
    "author": "Optima ICT Services LTD",
    "website": "http://www.optima.co.ke",
    "images": ["static/description/ipay.png"],
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Accounting",
    # "version": "16.0.0.1",
    "price": 149,
    "currency": "EUR",
    # any module necessary for this one to work correctly
    "depends": ["payment"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/ipay_views.xml",
        "views/templates.xml",
        "data/ipay_acquirer_data.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
    "application": True,
}
