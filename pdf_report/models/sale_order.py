from odoo import api, models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shipping_info = fields.Html("Shipping Info")
    wo_incoterm = fields.Char("WO Incoterm")
    is_mml_report_format = fields.Selection(related='company_id.report_format', string="MML Report Format", readonly=True)
    proforma_inv_prices = fields.Text(string='Prices',
                                      default='Price CPT Loughborough University according to incoterms 2020, shown in £ sterling. Exclusive of VAT unless stated.')
    proforma_inv_delivery = fields.Text(string='Delivery',
                                        default='Currently available 6 weeks after receipt of official Purchase Order')
    proforma_inv_delivery_days = fields.Text(string='Delivery Days',
                                             default='This quotation is valid for 90 days from the date of issue.')

    proforma_invoice_number = fields.Char(string="Proforma Invoice Number", compute="get_proforma_invoice")

    # https://spantech.odoo.com/web#id=623&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
    special_requirements = fields.Html(string="Special Requirements")
    reason_for_export =  fields.Text(string='Reason For Export')

    # https://spantech.odoo.com/web#id=857&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    partner_requirement = fields.Text(related='partner_id.requirement', readonly=False, groups="sales_team.group_sale_manager")

    # https://spantech.odoo.com/web#id=591&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
    client_order_rfq = fields.Char(string='Customer RFQ', copy=False)

    # https://spantech.odoo.com/web#id=915&menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5&action=806&model=project.task&view_type=form
    # lead_time_sp = fields.Date(string="Lead Time")
    lead_time_sp = fields.Char(string="Lead Time")

    def get_proforma_invoice(self):
        """
        Use:
        Added by: Jignesh
        Added on: 16/9/22
        Task: https://spantech.odoo.com/web#id=592&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
        """
        for sale in self:
            sale.proforma_invoice_number = sale.name.replace('WO', 'PI')

    def action_order_confirmation_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self._find_mail_template()
        lang = self.env.context.get('lang')
        # template = self.env['mail.template'].browse(template_id.id)
        # if template.lang:
        #     lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'confirmation': self.env.context.get('confirmation', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
