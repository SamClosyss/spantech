from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_tmpl_notes = fields.Text(related='product_id.product_tmpl_id.x_studio_product_notes',
                                     string='Product Notes')
    product_tmpl_hs_code = fields.Char(related='product_id.product_tmpl_id.x_studio_hs_code',
                                       string='Product HS Code')
    product_tmpl_country_of_origin = fields.Char(related='product_id.product_tmpl_id.x_studio_hs_code_1',
                                                 string='Product Country of Origin')
    product_tmpl_additional_description = fields.Text(
        related='product_id.product_tmpl_id.x_studio_additional_description',
        string='Additional Description')

    # @api.onchange('product_id')
    # def product_id_change(self):
    #     domain = super(SaleOrderLine, self).product_id_change()
    #     if self.product_id and self.order_id.sale_order_template_id:
    #         for line in self.order_id.sale_order_template_id.sale_order_template_line_ids:
    #             if line.product_id == self.product_id:
    #                 self.name = line.with_context(
    #                     lang=self.order_id.partner_id.lang).name + self._get_sale_order_line_multiline_description_variants()
    #                 break
    #     return domain
