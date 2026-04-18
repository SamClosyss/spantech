from odoo import api, fields, models, _


class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    def send_and_print_action(self):
        self.ensure_one()
        res = super(AccountInvoiceSend, self).send_and_print_action()
        if self.invoice_ids:
            self.invoice_ids.write({'invoice_confirmation_sent': 'yes'})
        return res
