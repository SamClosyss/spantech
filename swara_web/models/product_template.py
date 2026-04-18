# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class WebsiteMenu(models.Model):
    _inherit = 'product.template'

    collection_id = fields.Many2one('swara.collections', string="Product Collection")
    website_label = fields.Char("Website Label")