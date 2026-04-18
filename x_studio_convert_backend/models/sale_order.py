from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_studio_project_name = fields.Char(string='Project Name')
