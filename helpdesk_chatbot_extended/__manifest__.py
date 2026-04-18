{

    # App information
    'name': 'Helpdesk Chatbot Extended',
    'category': 'Services/Helpdesk',
    # 'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'This Module Is Used To Send Email From Chatbot.',
    'description': """
    This Module Is Used To Send Email From Chatbot.
        """,

    # Dependencies
    'depends': ['im_livechat'],

    'data': [
        'data/mail_template_data.xml',
        'views/chatbot_script_step_views.xml'
    ],

    'assets': {
    },

    # Odoo Store Specific
    'images': [],

    # Author
    'author': 'Cognifyx Technologies Pvt Ltd',
    'website': '',
    'maintainer': 'Jignesh',

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
