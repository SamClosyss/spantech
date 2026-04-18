{

    # App information
    'name': 'Little Swara Website',
    'category': 'website',
    # 'version': '16.0.1.0.0',
    'summary': 'Little Swara Website Shop',
    'license': 'LGPL-3',
    'description': """
        """,

    # Dependencies
    'depends': [
        'website_sale', 'mass_mailing'
    ],

    'data': [
        'views/product_template.xml',
        'views/website.xml',
        'views/swara_collections.xml',
        # 'views/swara_header.xml',
        # 'views/swara_footer.xml',
        'views/collection_template.xml',
        'security/ir.model.access.csv'

    ],
    'assets': {
        'web.assets_frontend': [
            # Css
            # 'swara_web/static/src/css/swara_web.scss',
     # 'swara_web/static/src/css/slick.css',
     # 'swara_web/static/src/css/main.css',

            # JS
            'swara_web/static/src/js/cart_popover.js',
            'swara_web/static/src/js/swara_script.js',
	    'swara_web/static/src/js/slick.min.js',
	    'swara_web/static/src/js/main.js',	
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
