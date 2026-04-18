{

    # App information
    'name': 'Website Image Category',
    'category': 'Website/Website',
    # 'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'Website Image Category',
    'description': """
        """,

    # Dependencies
    'depends': ['website_sale'],

    'data': [
        'views/product_page.xml',
        'views/product_template_views.xml'

    ],
    'assets': {
        'web.assets_frontend': [
            # 'website_image_categories/static/src/scss/product_variants.scss',
        ],
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
