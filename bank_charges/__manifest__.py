# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': 'Bank Charges',
    # 'version': '15.0.1.0',
    'summary': 'This module allows to have separate Journal entry for the bank charges',
    'description': """This Module Allows To Add Bank Charges When Make Payment Of Invoices.
    """,
    'category': 'Accounting/Accounting',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'images': ['static/description/banner.jpg'],
    'depends': ['account', 'account_tax_python', 'base_vat'],
    'data': [
        'views/bank_charges_view.xml'
    ],
    'sequence': 1,
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 20,
    'currency': 'EUR',
}
