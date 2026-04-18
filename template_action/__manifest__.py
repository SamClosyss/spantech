{
    'name': 'Template Action',
    # 'version': '16.0.0.1',
    'summary': 'Module to create many templates, actions, and models',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'category': 'Template Action',
    'depends': ['base', 'mail', 'sale_renting', 'pdf_report'],
    'data': [
        'security/ir.model.access.csv',
        'views/template_action_views.xml',
    ],
    'installable': True,
    'application': True,
}