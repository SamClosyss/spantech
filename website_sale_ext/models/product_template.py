from odoo import api, fields, models, Command


# https://spantech.odoo.com/web?debug=1#id=1020&menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5%2C10%2C9&action=806&model=project.task&view_type=form
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False,
                              parent_combination=False, only_template=False):
        combination_info = super()._get_combination_info(combination=combination, product_id=product_id,
                                                         add_qty=add_qty, pricelist=pricelist,
                                                         parent_combination=parent_combination,
                                                         only_template=only_template)

        if combination_info['product_id']:
            combination_info['display_notification'] = False if self.env.company.report_format in ['lss_serbia_report','spantech_report'] else True
            website = self.env['website'].get_current_website()
            product_variant_id = self.env['product.product'].browse(combination_info['product_id'])
            if website:
                combination_info['stock_in_msg'] = website.stock_in_custom_msg
                if product_variant_id.product_display_name:
                    combination_info['display_name'] = product_variant_id.product_display_name
                else:
                    # combination_info['display_name'] = product_variant_id.display_name
                    name = ""
                    i = 1
                    for ptav in product_variant_id.product_template_attribute_value_ids:
                        name += '%s' % (ptav.display_name.split(":")[1]).strip()
                        if not i == len(product_variant_id.product_template_attribute_value_ids):
                            name += ','
                            i += 1
                    combination_info['display_name'] = "%s(%s)" % (product_variant_id.name, name)
        return combination_info


    # @api.model
    # def _price_with_tax_computed(
    #     self, price, product_taxes, taxes, company_id, pricelist, product, partner
    # ):
    #     price = self.env['product.product']._get_tax_included_unit_price_from_price(
    #         price,
    #         pricelist.currency_id,
    #         product_taxes,
    #         product_taxes_after_fp=taxes,
    #     )
    #     show_tax_excluded = self.user_has_groups('account.group_show_line_subtotals_tax_excluded')
    #     # tax_display = 'total_excluded' if show_tax_excluded else 'total_included'
    #     if self.website_id.show_line_subtotals_tax_selection == 'tax_excluded':
    #         tax_display = 'total_excluded'
    #     elif self.website_id.show_line_subtotals_tax_selection == 'tax_included':
    #         tax_display = 'total_included'
    #     else:
    #         tax_display = 'total_excluded' if show_tax_excluded else 'total_included'
    #     # The list_price is always the price of one.
    #     return taxes.compute_all(price, pricelist.currency_id, 1, product, partner)[tax_display]


class Productproduct(models.Model):
    _inherit = 'product.product'

    product_display_name = fields.Char(string="Product Display Name",
                                       help="Display Variant Custom Name to Website Product Page")
