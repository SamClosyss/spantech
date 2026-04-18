from odoo import fields, api, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_order_sent = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='SCS', readonly=True,
                                       copy=False, index=True, default='no', help="Sales Confirmation Sent")

    # https://spantech.odoo.com/web#id=480&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
    is_IGM_customer = fields.Boolean(string="Is Requires in IGM", related="partner_id.is_IGM_customer")
    partner_responsible_rep = fields.Many2one(related="partner_id.partner_responsible_rep", string='Responsible Rep', tracking=True,
                                      readonly=False)
    consignee_name = fields.Char(string="Consignee Name")
    notify_party = fields.Char(string="Notify Party")
    value_for_customs_with_currency = fields.Char(string="Value For Customs with Currency")
    manifested_gross_weight = fields.Char(string="Manifested Gross Weight")
    manifested_packages = fields.Char(string="Manifested Packages")
    description_of_goods = fields.Char(string="Descrition of Goods")

    # https://spantech.odoo.com/web?debug=1#id=482&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    partner_contact_id = fields.Many2one('res.partner', string='Contact Name', domain="[('parent_id','=',partner_id)]")

    # @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        """
        Use: Add confirmation sent flag SPL sales overview
        Added by: Jignesh
        Added on: 24/6/22
        Task: https://spantech.odoo.com/web?debug=1#id=313&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
        """
        rec = super(SaleOrder, self).message_post(**kwargs)
        if self.env.context.get('mark_so_as_sent'):
            self.filtered(lambda o: o.state == 'sale').write({'sale_order_sent': 'yes'})
        return rec

    # https://spantech.odoo.com/web?debug=1#id=313&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        self.write({'sale_order_sent': 'no'})
        return res

    def create_po_without_confirm_order(self):
        """
        Use: Create PO without Confirm Order
        Added by: Jignesh
        Added on: 22/6/22
        Task: https://spantech.odoo.com/web?debug=1#id=311&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
        """
        self.ensure_one()
        self.with_context(tracking_disable=True).action_confirm()
        self.with_context(tracking_disable=True).action_cancel()
        self.with_context(tracking_disable=True).action_draft()
        # if self.picking_ids:
        #     self.picking_ids.unlink()
        if self.purchase_order_count > 0:
            msg_body = _("Purchase Order Created Using Create Po Button")
            self.message_post(body=msg_body)
            return {
                'effect': {
                    'type': 'rainbow_man',
                    'message': _('Yeah! Successfully Create Purchase Order.'),
                }
            }
        return True

    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(SaleOrder, self).create(vals)
    #     for sale in res:
    #         # https://spantech.odoo.com/web#id=652&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
    #         if sale.partner_id and sale.partner_id.x_studio_many2one_field_5MK2F:
    #             sale.incoterm = sale.partner_id.x_studio_many2one_field_5MK2F.id
    #     return res

    @api.onchange('partner_id', 'partner_id.x_studio_many2one_field_5MK2F')
    def onchange_partner_id(self):
        """
        Use: Set Partner Incotern to Sale Order
        Added by: Jignesh
        Added on: 2/11/22
        Task: https://spantech.odoo.com/web#id=652&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
        """
        # super(SaleOrder, self).onchange_partner_id()
        if self.partner_id and self.partner_id.x_studio_many2one_field_5MK2F:
            self.incoterm = self.partner_id.x_studio_many2one_field_5MK2F.id
        if self.partner_id and self.partner_id.property_payment_term_id:
            self.payment_term_id = self.partner_id.property_payment_term_id.id

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        res['payment_term_id'] = False
        return res
