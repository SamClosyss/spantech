# ©  2008-2021 Deltatech
# See README.rst file on addons root folder for license details
{
    "name": "Revolut Payment Provider",
    "summary": "Revolut Payment Provider",
    # "version": "16.0.0.0.5",
    "author": "Terrabit, Dorin Hongu",
    "website": "https://www.terrabit.ro",
    "support": "odoo@terrabit.ro",
    "category": "Accounting",
    "depends": [
        "payment",
    ],
    "data": ["views/payment_templates.xml", "views/payment_views.xml", "data/payment_acquirer_data.xml"],
    "assets": {
        "web.assets_frontend": [
            "deltatech_payment_revolut/static/src/js/payment_form.js",
        ],
    },
    "price": 220.00,
    "currency": "EUR",
    "license": "OPL-1",
    "images": ["static/description/main_screenshot.png"],
    "development_status": "Beta",
    "maintainers": ["dhongu"],
    "extra_buy": True,
}
