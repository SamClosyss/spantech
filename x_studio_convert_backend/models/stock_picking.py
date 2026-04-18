from odoo import models, api, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    delivery_notes = fields.Html(string='Delivery Notes', translate=True)
