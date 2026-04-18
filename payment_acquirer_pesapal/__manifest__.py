# -*- coding: utf-8 -*-
# Copyright (c) 2022-Present Mentis Consultancy Services. (<https://mcss.odoo.com>)

{
    'name': 'Pesapal Payment Provider',
    'category': 'Accounting/Payment Providers',
    # 'version': '16.0.1.1',
    'license': 'OPL-1',
    'author': 'Mentis Consultancy Services',
    'website': 'https://mcss.odoo.com',
    'depends': ['payment'],
    'data': [
        'views/payment_pesapal_templates.xml',
        'views/payment_views.xml',
        'data/payment_provider_data.xml',
    ],
    'images': [
        'static/description/banner.gif',
    ],
    'application': True,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'description': """Pesapal Payment Provider""",
    'price': 149,
    'currency': 'EUR',
    'summary': '''
        Payment Provider: Pesapal Payment Gateway
        Online Payment
        E-commerce Payment
        Invoice Payment
        Debit Card Payment
        Credit Card Payment
    '''
}
