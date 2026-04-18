{

    # App information
    'name': 'X_Studio Changes Convert in Backend',
    'category': 'Customization',
    # 'version': '16.0.1.0.0',
    'summary': 'Added x_studio changes in backend',
    'license': 'LGPL-3',
    'description': """
    Inform to customer like don't directly add change using studio and created this module on 24MAY2022 Database 
        """,

    # Dependencies
    'depends': ['hr_expense','mrp','project','crm','delivery', 'purchase', 'sale_stock'],

    'data': [
        'views/hr_expense_views.xml',
        'views/product_views.xml',
        'views/project_views.xml',
        'views/purchase_views.xml',
        'views/res_partner_views.xml',
        'views/res_users_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
        'views/crm_lead_views.xml',
    ],

    # Odoo Store Specific
    'images': [],

    # Author
    'author': 'Jignesh',
    'website': '',
    'maintainer': 'Jignesh',

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
