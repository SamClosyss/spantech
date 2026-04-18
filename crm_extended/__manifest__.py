{

    # App information
    'name': 'CRM Extended',
    'category': 'Sales/CRM',
    # 'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'CRM Extended for Spantech',
    'description': """
        """,

    # Dependencies
    'depends': ['crm', 'sale_stock_extended'],

    'data': [
        'views/crm_lead_views.xml',
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
