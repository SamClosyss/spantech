from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_tmpl_notes = fields.Text(related='product_id.product_tmpl_id.x_studio_product_notes',
                                     string='Product Notes')
    product_tmpl_hs_code = fields.Char(related='product_id.product_tmpl_id.x_studio_hs_code',
                                       string='Product HS Code')
    product_tmpl_country_of_origin = fields.Char(related='product_id.product_tmpl_id.x_studio_hs_code_1',
                                                 string='Product Country of Origin')

    # @api.onchange('product_id')
    # def onchange_product_id(self):
    #     res = super(PurchaseOrderLine, self).onchange_product_id()
    #     if self.product_id and self.name and self.product_id.product_tmpl_id.x_studio_product_notes:
    #         self.name = self.name + '\nProduct Notes: ' + self.product_id.product_tmpl_id.x_studio_product_notes
    #     return res
