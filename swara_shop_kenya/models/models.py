from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    web_name = fields.Char(string='Website Name')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['web_name'] = self.env['ir.config_parameter'].sudo().get_param('swara_shop_kenya.web_name')
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('swara_shop_kenya.web_name', self.web_name)
        super(ResConfigSettings, self).set_values()


class ProductInherit(models.Model):
    _inherit = 'product.product'

    featured = fields.Boolean('Featured')