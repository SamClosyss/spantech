# -*- coding: utf-8 -*-
from odoo import _, api, fields, models

class Website(models.Model):
    _inherit = 'website'

    home_product_ids = fields.Many2many('product.template', string="Home Page Products" , domain="[('type', '=', 'product')]",)
    collection_1_name = fields.Char("First collection Label")
    collection_1_image = fields.Image("First collection Image", max_width=1920, max_height=1080)
    collection_1_url = fields.Char("First collection Url")
    collection_2_name = fields.Char("Second collection Label")
    collection_2_image = fields.Image("Second collection Image", max_width=1920, max_height=1080)
    collection_2_url = fields.Char("Second collection Url")
    collection_3_name = fields.Char("Third collection Label")
    collection_3_image = fields.Image("Third collection Image", max_width=1920, max_height=1080)
    collection_3_url = fields.Char("Third collection Url")

    def collection_details(self,key=False):
        if key and key == 1:
            #/web/image/website/%s/collection_%s_image/'%(request.website.id,key)
            return {'string':self.collection_1_name,'image':'/web/image/website/%s/collection_1_image/'%(self.id),'url':self.collection_1_url}
        if key and key == 2:
            #/web/image/website/%s/collection_%s_image/'%(request.website.id,key)
            return {'string':self.collection_2_name,'image':'/web/image/website/%s/collection_2_image/'%(self.id),'url':self.collection_2_url}
        if key and key == 3:
            #/web/image/website/%s/collection_%s_image/'%(request.website.id,key)
            return {'string':self.collection_3_name,'image':'/web/image/website/%s/collection_3_image/'%(self.id),'url':self.collection_3_url}
