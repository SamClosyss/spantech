{

    # App information
    'name': 'PDF Report for Spantech',
    'category': 'Customization/Report',
    # 'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'summary': 'Add new layout to report templates',
    'description': """
        """,

    # Dependencies
    'depends': ['account', 'sale','purchase', 'x_studio_convert_backend', 'stock_picking_invoice_link'],

    'data': [
        'security/ir.model.access.csv',
        'data/paper_format.xml',
        'report/report_invoice.xml',
        'data/report_action.xml',
        'data/aggases_report_action.xml',
        'data/mail_template_data.xml',
        'report/mml_report_common.xml',
        'report/spantech_report_common.xml',
        'report/spantech_report_purchase.xml',
        'report/report_sale_order.xml',
        'report/report_deliveryslip.xml',
        'report/report_mrp_production.xml',
        'report/mml_report_invoice.xml',
        'report/mml_report_sale_order.xml',
        'report/sspzoo_invoice_document.xml',
        'report/sspzoo_purchase_document.xml',
        'report/spz_report_sale_order.xml',
        'report/spz_report_delivery_document.xml',
        'report/mml_report_purchase_quotation.xml',
        'report/mml_report_purchase_order.xml',
        'report/mml_report_sale_proforma_invoice.xml',
        'report/report_purchase_order.xml',
        'report/ag_gases_report_deliveryslip.xml',
        'report/ag_gases_report_sale_order.xml',
        'report/ag_gases_report_purchase_quotation.xml',
        'report/ag_gases_report_invoice.xml',
        'report/ag_gases_report_shipping_invoice.xml',
        'report/mml_report_shipping_invoice.xml',
        'report/ag_gases_report_production_order.xml',
        'report/ag_gases_certificate_report.xml',
        'report/ag_gases_bottle_label_report.xml',
        'report/report_rental_order_document_ext.xml',
        'report/lss_report.xml',
        'report/ag_gases_cac_certificate_report.xml',
        'report/ag_gases_cac_label_report.xml',
        'report/ag_gases_qrcode_report.xml',
        'report/all_in_gas_label_report.xml',
        'report/cac_box_label_report.xml',
        'report/kimessa_label_report.xml',
        'report/all_in_gas_certificate_report.xml',
        'report/cac_nkd_label_report.xml',
        'report/all_in_gas_label_krapp_report.xml',
        # New 9 reports
        'report/gas_tech_report_pdf.xml',
        'report/gas_alarm_report_pdf.xml',
        'report/encore_monitoring_report_pdf.xml',
        'report/CAC_gas_asia_report_pdf.xml',
        'report/CAC_gas_instrumentation_report_pdf.xml',
        'report/NZ_safety_blackwoods_report_pdf.xml',
        'report/mine_safety_report_pdf.xml',
        'report/skillpro_report_pdf.xml',
        'report/alliance_safety_report_pdf.xml',
        
        'views/sale_views.xml',
        'report/spzoo_wip_label.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/mrp_production_views.xml',
        'views/product_views.xml',

    ],
    'assets': {
        'web.report_assets_pdf': [
            'pdf_report/static/src/scss/report_action.scss',
        ],
        'web.report_assets_common': [
            'pdf_report/static/src/scss/report_action.scss',
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
