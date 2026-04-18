from odoo import _, models, fields


class ChatbotScriptStep(models.Model):
    _inherit = 'chatbot.script.step'

    is_sent_mail = fields.Boolean(string='Send Email?')
    email = fields.Char("Emails Ids")
    # domain="[('model', '=', 'im_livechat.model_chatbot_script_step')]",
    email_template_id = fields.Many2one('mail.template', string='Chatbot Email Template')

    def _process_step(self, mail_channel):
        self.ensure_one()
        posted_message = super()._process_step(mail_channel)
        if self.is_sent_mail and self.email:
            self._process_step_send_email(mail_channel)
        return posted_message

    def _process_step_send_email(self, mail_channel):
        if not self.email_template_id:
            email_templ = self.env.ref("helpdesk_chatbot_extended.email_template_chatbot", raise_if_not_found=False)
        else:
            email_templ = self.email_template_id
        customer_values = self._chatbot_prepare_customer_values(mail_channel, create_partner=False,
                                                                update_partner=False)
        ctx = self.env.context.copy()
        ctx.update({'description': customer_values['description'] + mail_channel._get_channel_history()})
        # email_templ.sudo().with_context(ctx).send_mail(self.id, force_send=True)
        email_templ.sudo().with_context(ctx).send_mail(self.id, email_values={'email_to': self.email}, force_send=True)
        self.env['mail.mail'].process_email_queue()
        # customer_values = self._chatbot_prepare_customer_values(
        #     mail_channel, create_partner=False, update_partner=True)
        # if customer_values.get('email', False):
        #     email_templ = self.env.ref("helpdesk_chatbot_extended.email_template_chatbot")
        #     email_templ.sudo().send_mail(self.id, email_values={'email_to': customer_values.get('email', False)},
        #                                  force_send=True)
