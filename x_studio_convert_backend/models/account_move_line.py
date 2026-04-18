from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_tmpl_notes = fields.Text(related='product_id.product_tmpl_id.x_studio_product_notes',
                                     string='Product Notes')
    product_tmpl_hs_code = fields.Char(related='product_id.product_tmpl_id.x_studio_hs_code',
                                       string='Product HS Code')
    product_tmpl_country_of_origin = fields.Char(related='product_id.product_tmpl_id.x_studio_hs_code_1',
                                                 string='Product Country of Origin')
