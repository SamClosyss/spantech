from odoo import fields, models, api

REPORT_FORMAT = [('default', 'Default'),
                 ('spantech_report', 'Spantech Report Header/Footer'),
                 ('ag_gases_report', 'AG Gases Report Header/Footer'),
                 ('MML_report', 'MML Report Header/Footer'),
                 ('spancan_n_equipment_report', 'Spancan n Equipment Report Header/Footer'),
                 ('sspzoo_report', 'Spantech SP Zoo Reports'),
                 ('lss_serbia_report', 'LSS Serbia'),
                 ('mjs_report', 'MJS Report Header/Footer'),]


class ResCompany(models.Model):
    _inherit = "res.company"

    report_format = fields.Selection(REPORT_FORMAT, string="Report Header/Footer", default="default", required=True)

class BaseDocumentLayout(models.TransientModel):
    _inherit = "base.document.layout"
    
    report_format = fields.Selection(REPORT_FORMAT, string="Report Header/Footer", default="default", required=True)
