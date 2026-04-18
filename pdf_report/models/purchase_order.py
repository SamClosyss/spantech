from odoo import api, models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # https://spantech.odoo.com/web#id=623&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
    special_requirements = fields.Html(string="Special Requirements")
    
    
    
    def print_quotation(self):
        self.write({'state': "sent"})
        return self.env.ref('pdf_report.mml_report_purchase_quotation').report_action(self)
