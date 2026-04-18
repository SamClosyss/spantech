from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    delivery_approx_time = fields.Char('Delivery Note')