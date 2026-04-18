from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.product'

    product_variants_image_ids = fields.One2many('product.image', 'product_variant_id',
                                                 string="Extra Product Variants Images")

    def _get_images(self):
        self.ensure_one()
        variant_images = list(self.product_variant_image_ids)
        if self.image_variant_1920:
            variant_images = [self] + variant_images
        else:
            variant_images = [self] + variant_images
        return variant_images + self.product_tmpl_id._get_images()[1:]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    image_attribute_lines = fields.One2many('product.template.attribute.value', 'product_tmpl_id', string='Order Lines')

    def set_varinat_images(self):
        ptavs = self.env['product.template.attribute.value'].search([('product_tmpl_id', '=', self.id)])
        for ptav in ptavs:
            if not ptav.attribute_id.display_type == 'color':
                continue
            if not ptav.image:
                continue
            prods = self.env['product.product'].search([('product_template_attribute_value_ids', 'in', [ptav.id])])
            for prod in prods:
                prod.sudo().write({
                    'image_variant_1920': ptav.image
                })


class ProductTemplateAttributeLine(models.Model):
    _inherit = 'product.template.attribute.value'

    image = fields.Image("Image")


#prod_temps = self.env['product.template'].search([])
#        for pt in prod_temps:
#          pt.set_varinat_images()
