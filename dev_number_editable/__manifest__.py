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
    'name': 'Number Editable in Sale/Purchase/Invoice',
    # 'version': '1.0',
    'license': 'LGPL-3',
    'sequence': 1,
    'category': 'Sales',
    'description':
         """
odoo app will help to edit number after confirm/validat sale, purchase,invoice 
        
        Number editable 
        Odoo number editable 
        Odoo sale order number edit
        Odoo purchase number edit
        odoo invoice number edit
        edit number after sale confirm in odoo
        edit number after purchase confirm in odoo
        edit number after Invocie confirm in odoo
Number editable
Odoo number editable
Edit sale / purchase / invoice number
Odoo edit sale / purchase / invoice number
Edit sale number
Odoo edit sale number
Edit purchase number
Odoo edit purchase number
Edit invoice number
Odoo edit invoice number
Easy to edit sale number
Odoo easy to edit sale number
Easy to edit purchase number
Odoo easy to edit purchase number
Easy to edit invoice number
Odoo easy to edit invoice number
Manage sale number edit
Odoo manage sale number edit
Manage purchase number edit
Odoo manage purchase number edit
Manage invoice number edit
Odoo manage invoice number edit        

         """,
    'summary': 'odoo app will help to edit number after confirm/validat sale, purchase,invoice,Number editable,Sale number editable, Invoice number editable, purchase number editable ',
    'depends': ['sale_management','purchase'],
    'data': [
        'security/security_group.xml',
        'views/sale_order_view.xml',
        'views/purchasae_order_view.xml',
        'views/invoice_view.xml',
        
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    #author and support Details
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':19.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
    # 'pre_init_hook' :'pre_init_check',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
