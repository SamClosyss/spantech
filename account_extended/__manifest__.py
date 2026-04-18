{

    # App information
    'name': 'Account Extended',
    'category': 'Accounting/Accounting',
    # 'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'Account Extended for Spantech',
    'description': """
        """,

    # Dependencies
    'depends': ['sale', 'account_followup'],

    'data': [
        'data/account_followup_data.xml',
        'views/account_move_views.xml',
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
