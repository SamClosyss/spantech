# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class SwaraCollections(models.Model):
    _name = 'swara.collections'

    sequence = fields.Integer(default=10)
    name = fields.Char(string='Name')
    description = fields.Html(string="Description", translate=True)
    image = fields.Image("Collection Banner Image", max_width=1920, max_height=1080)
    product_tmpl_ids = fields.One2many('product.template', 'id', string='Product Ids', compute='_compute_products')
    product_ids = fields.Many2many('product.template', string="Related Products", domain="[('type', '=', 'product')]",)

    def _compute_products(self):
        for cl in self:
            cl.product_tmpl_ids = self.env['product.template'].sudo().search([('collection_id', '=', self.id)])

    @api.model
    def clean_url(self):
        # return '/collection/%s/-%s' % (self.name.replace(r' ','-').lower(), self.id)
        return '/collection/%s' % self.id
