from odoo import fields, api, models, _
from lxml import etree


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def action_quotation_send(self):
        res = super(SaleOrder, self).action_quotation_send()
        action_id = False
        if self._context.get('default_is_rental_order') == 1:
            action_id = self.env.ref('sale_renting.rental_order_action').id
        elif self.state in ('draft','sent'):
            action_id = self.env.ref('sale.action_quotations_with_onboarding').id
        elif self.state not in ('draft','sent','cancel'):
            action_id = self.env.ref('sale.action_orders').id
        elif self.invoice_status == 'to invoice':
            action_id = self.env.ref('sale.action_orders_to_invoice').id
        elif self.invoice_status == 'upselling':
            action_id = self.env.ref('sale.action_orders_upselling').id
        template_action = self.env['template.action'].search([
                ('action_id', '=', action_id),
                ('company_id', '=', self.company_id.id),
                ('active', '=', True)
            ], limit=1)
        if template_action.id and template_action.email_template_id.id:
            mail_template = template_action.email_template_id
            res['context'].update({'default_template_id': mail_template.id})
            mail_compose = self.env['mail.compose.message'].search([
                ('model', '=', 'sale.order'),
                ('template_id', '=', mail_template.id)
            ], limit=1)
            if mail_compose:
                mail_compose.template_id.report_template = template_action.pdf_report_id.id
        return res

    def action_order_confirmation_send(self):
        res = super(SaleOrder, self).action_order_confirmation_send()
        action_id = False
        if self._context.get('default_is_rental_order') == 1:
            action_id = self.env.ref('sale_renting.rental_order_action').id
        elif self.state in ('draft','sent'):
            action_id = self.env.ref('sale.action_quotations_with_onboarding').id
        elif self.state not in ('draft','sent','cancel'):
            action_id = self.env.ref('sale.action_orders').id
        elif self.invoice_status == 'to invoice':
            action_id = self.env.ref('sale.action_orders_to_invoice').id
        elif self.invoice_status == 'upselling':
            action_id = self.env.ref('sale.action_orders_upselling').id
        template_action = self.env['template.action'].search([
                ('action_id', '=', action_id),
                ('company_id', '=', self.company_id.id),
                ('active', '=', True)
            ], limit=1)
        if template_action.id and template_action.email_template_id.id:
            mail_template = template_action.email_template_id
            res['context'].update({'default_template_id': mail_template.id})
            mail_compose = self.env['mail.compose.message'].search([
                ('model', '=', 'sale.order'),
                ('template_id', '=', mail_template.id)
            ], limit=1)
            if mail_compose:
                mail_compose.template_id.report_template = template_action.pdf_report_id.id
        return res
