{

    # App information
    'name': 'Helpdesk Extended',
    'category': 'Services/Helpdesk',
    # 'version': '16.0.1.0.0',
    'summary': 'Helpdesk Extended for Spantech',
    'license': 'LGPL-3',
    'description': """
        """,

    # Dependencies
    'depends': ['helpdesk', 'x_studio_convert_backend'],

    'data': [
        'views/helpdesk_ticket_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/helpdesk_team_view.xml',
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
