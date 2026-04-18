from odoo import api, models, fields
import re


class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_order_id = fields.Many2one(comodel_name='sale.order', string="Sale Order", compute='_compute_sale_order_id',
                                    store=True)

    # https://spantech.odoo.com/web?debug=1#id=904&menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5%2C10%2C9&action=806&model=project.task&view_type=form
    picking_schedule_date = fields.Datetime('Picking Scheduled Date', copy=False,
                                            help="Add this field data into shipping invoice report of AG Gases")

    picking_date_done = fields.Datetime('Picking Date', copy=False,
                                            help="Add this field data into shipping invoice report of MML")
    picking_user_id = fields.Many2one("res.users", string="Picking User")
    picking_packages_number = fields.Integer(string="Picking packages Number")
    picking_delivery_note = fields.Html(string='Picking Comment')

    @api.depends('invoice_line_ids.sale_line_ids.order_id')
    def _compute_sale_order_id(self):
        for rec in self:
            rec.sale_order_id = rec.mapped('invoice_line_ids.sale_line_ids.order_id')[:1]

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        # https://spantech.odoo.com/web?debug=1#id=410&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
        if self.partner_id.x_studio_many2one_field_5MK2F:
            self.invoice_incoterm_id = self.partner_id.x_studio_many2one_field_5MK2F
        return res



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def parse_float(self, value):
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            match = re.search(r'[-+]?[0-9]*\.?[0-9]+', value)
            if match:
                return float(match.group())
        return 0.0

    subtotal_net_weight = fields.Float(string="Sub Total Net Weight", compute="_compute_subtotal_net_weight")
    subtotal_gross_weight = fields.Float(string="Sub Total Gross Weight", compute="_compute_subtotal_gross_weight")

    def _compute_subtotal_net_weight(self):
        for rec in self:
            net_weight = rec.parse_float(rec.product_id.net_weight)
            quantity = rec.quantity
            rec.subtotal_net_weight = round((net_weight * quantity), 2) if net_weight else 0.0

    def _compute_subtotal_gross_weight(self):
        for rec in self:
            gross_weight = rec.parse_float(rec.product_id.gross_weight)
            quantity = rec.quantity

            rec.subtotal_gross_weight = round((gross_weight * quantity), 2) if gross_weight else 0.0
