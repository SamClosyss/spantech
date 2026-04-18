{

    # App information
    'name': 'Sale Stock Extended',
    'category': 'Sales/Sales',
    # 'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'Sale Stock Extended for Spantech',
    'description': """
        """,

    # Dependencies
    'depends': ['sale_purchase'],

    'data': [
        'data/data.xml',
        'data/mail_template_data.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
    ],

    'assets': {
    },

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
