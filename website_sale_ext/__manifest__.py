{

    # App information
    'name': 'Website Sale Extended',
    # 'version': '16.0.0',
    'category': 'Website/Website',
    'license': 'LGPL-3',
    'summary': """ 
    1.Add Variant full name in the product webpage
    2. Website Attribute change design
        """,
    'description': """
        """,

    # Dependencies
    'depends': ['website_sale','website_sale_stock'],

    'data': [
        'views/product_product.xml',
        'views/template.xml',
        # 'views/product_page.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/ir_attachment_views.xml',
        'views/website_views.xml',
        'views/sale_order_view.xml',
    ],
    'assets': {
        # 'web.assets_frontend': [
        #     'website_sale_ext/static/src/js/website_sale_script.js',
        #     'website_sale_ext/static/src/scss/style.scss',
        # ],
        'web.assets_frontend': [
            ('after', 'website/static/src/scss/website.scss', 'website_sale_ext/static/src/scss/menu.scss'),
            'website_sale_ext/static/src/js/website_sale_script.js',
            'website_sale_ext/static/src/scss/style.scss',
            'website_sale_ext/static/src/js/menu.js',
            'website_sale_ext/static/src/xml/stock_notification.xml',
            'website_sale_ext/static/src/js/shop_attribute_accordian.js'
        ],
        'website.assets_editor': [
            'website_sale_ext/static/src/js/edit_menu_extended.js',
        ],
        'website.assets_wysiwyg': [
            'website_sale_ext/static/src/snippets/embed_video/options.js',
            'website_sale_ext/static/src/xml/video_edit.xml',
        ]
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
