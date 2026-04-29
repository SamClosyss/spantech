# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Amount In Words-(IND) - Indian Format Amount in words',
    # 'version': '16.0.1.0',
    'sequence': 1,
    'category': 'Accounting',
    'description':
        """
 Apps will show toatl amount into words in Sale, Purchase, Invoice in Indian Currency Format

    """,
    'summary': 'Apps will show toatl amount into words in Sale, Purchase, Invoice in Indian Currency Format',
    'author': 'Devintelle Consulting Service Pvt.Ltd',
    'website': 'https://www.devintellecs.com',
    'depends': ['sale','account','purchase'],
    'data': [
        'view/sale_order_view.xml',
        'view/purchase_order_view.xml',
        'view/invoice_view.xml',
        'report/report_view.xml'
        ],
    'demo': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto-install':False,
    # 'pre_init_hook' :'pre_init_check',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
