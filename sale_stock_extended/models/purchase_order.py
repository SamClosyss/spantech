from odoo import fields, api, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_order_sent = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='POS', readonly=True,
                                           copy=False, index=True, default='no', help="Purchase Order Sent")

    # https://spantech.odoo.com/web?debug=1#id=748&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    tag_ids = fields.Many2many('crm.tag', 'purchase_order_tag_rel', 'purchase_order_id', 'tag_id', string='Tags')

    # @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        """
        Use: Creation of "purchase order sent flag"
        Added by: Jignesh
        Added on: 24/6/22
        Task: https://spantech.odoo.com/web?debug=1#id=314&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
        """
        rec = super(PurchaseOrder, self).message_post(**kwargs)
        if self.env.context.get('mark_rfq_as_sent'):
            self.filtered(lambda o: o.state == 'purchase').write({'purchase_order_sent': 'yes'})
        return rec

    # https://spantech.odoo.com/web?debug=1#id=314&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
    def button_cancel(self):
        res = super(PurchaseOrder, self).button_cancel()
        self.write({'purchase_order_sent': 'no'})
        return res

    @api.onchange('partner_id', 'company_id', 'partner_id.x_studio_many2one_field_5MK2F')
    def onchange_partner_id(self):
        """
        Use: Set Partner Incotern to Sale Order
        Added by: Jignesh
        Added on: 2/11/22
        Task: https://spantech.odoo.com/web#id=652&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
        """
        super(PurchaseOrder, self).onchange_partner_id()
        if self.partner_id and self.partner_id.x_studio_many2one_field_5MK2F:
            self.incoterm_id = self.partner_id.x_studio_many2one_field_5MK2F.id
