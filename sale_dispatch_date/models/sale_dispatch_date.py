# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    dispatch_date = fields.Datetime(string="Dispatch Date", tracking=True)
    delivery_done = fields.Boolean(string="Delivery Done", compute="_compute_delivery_done", store=True)

    @api.depends('picking_ids.state')
    def _compute_delivery_done(self):
        for order in self:
            if order.picking_ids:
                order.delivery_done = all(picking.state == 'done' for picking in order.picking_ids)
            else:
                order.delivery_done = False

    def action_so_dispatch_date(self):
        self.ensure_one()
        self.dispatch_date = fields.Datetime.now()
        self.message_post(
        body=f"Dispatch Date was set to {self.dispatch_date.strftime('%Y-%m-%d %H:%M:%S')} by {self.env.user.name}.",
        subtype_xmlid="mail.mt_note"
    )
