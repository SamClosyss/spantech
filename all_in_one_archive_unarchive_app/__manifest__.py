# -*- coding: utf-8 -*-

{
    'name' : 'All in One Archive and Unarchive Records',
    'author': "Edge Technologies",
    # 'version' : '16.0.1.0',
    'live_test_url':'https://youtu.be/tzb1BFqeVwY',
    'images':['static/description/main_screenshot.png'],
    'summary' : 'All in One Archive records all in one Unarchive records all archive all active records all inactive records all in one active all in one inactive active sales active invoice active inventory archive sales archive purchase active purchase invoice archive',
    'description' : """
            All in One Archive and Unarchive helps to archive and unarchive the records.
    """,
    'depends': ['base','sale_management','purchase','stock','account'],
    "license" : "OPL-1",
    'data': [
        'views/archive_order.xml',
    ],
    'qweb': [],
    'installable' : True,
    'auto_install' : False,
    'price': 28,
    'currency': 'EUR',
    'category' : 'Extra Tools',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
