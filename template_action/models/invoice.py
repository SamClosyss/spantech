from odoo import fields, api, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_invoice_sent(self):
        res = super(AccountMove, self).action_invoice_sent()
        action_id = False
        if self._context.get('default_move_type') == 'out_invoice':
            action_id = self.env.ref('account.action_move_out_invoice_type').id
        if self._context.get('default_move_type') == 'out_refund':
            action_id = self.env.ref('account.action_move_out_refund_type').id
        if self._context.get('default_move_type') == 'in_invoice':
            action_id = self.env.ref('account.action_move_in_invoice_type').id
        if self._context.get('default_move_type') == 'in_refund':
            action_id = self.env.ref('account.action_move_in_refund_type').id
        template_action = self.env['template.action'].search([
        ('action_id', '=', action_id),
        ('company_id', '=', self.company_id.id),
        ('active', '=', True)
        ], limit=1)
        if template_action.id and template_action.email_template_id.id:
            template_id = template_action.email_template_id.id
            res['context'].update({'default_template_id': template_id})
            mail_compose = self.env['mail.template'].search([
                ('model_id.model', '=', 'account.move'),
                ('id', '=', template_id)
            ], limit=1)
            if mail_compose:
                mail_compose.report_template = template_action.pdf_report_id.id
        return res
