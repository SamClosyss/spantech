# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

from odoo import fields, models, _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_bc_line = fields.Boolean(help="Technical Field")


class AccountJournal(models.Model):
    _inherit = "account.journal"

    default_bank_charge_account_id = fields.Many2one('account.account', string='Default Bank Charge Account', domain=[('deprecated', '=', False)])


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    bank_charges = fields.Float(string="Bank Charges")

    def _create_payment_vals_from_wizard(self, batch_result):
        res = super(AccountPaymentRegister, self)._create_payment_vals_from_wizard(batch_result)
        res.update({'bank_charges': self.bank_charges})
        return res


class AccountPayment(models.Model):
    _inherit = "account.payment"

    bank_charges = fields.Float(string="Bank Charges")

    def _seek_for_lines(self):
        ''' Helper used to dispatch the journal items between:
        - The lines using the temporary liquidity account.
        - The lines using the counterpart account.
        - The lines being the write-off lines.
        :return: (liquidity_lines, counterpart_lines, writeoff_lines)
        '''
        self.ensure_one()

        liquidity_lines = self.env['account.move.line']
        counterpart_lines = self.env['account.move.line']
        writeoff_lines = self.env['account.move.line']

        for line in self.move_id.line_ids.filtered(lambda x: not x.is_bc_line):
            if line.account_id in self._get_valid_liquidity_accounts():
                liquidity_lines += line
            elif line.account_id.account_type in ('asset_receivable', 'liability_payable') or line.partner_id == line.company_id.partner_id:
                counterpart_lines += line
            else:
                writeoff_lines += line

        return liquidity_lines, counterpart_lines, writeoff_lines

    def _create_bank_charges_entry(self):
        charges = [{
            'account_id': self.journal_id.default_account_id.id,
            'partner_id': self.payment_type in ('inbound', 'outbound') and self.env['res.partner']._find_accounting_partner(self.partner_id).id or False,
            'name': self.ref,
            'credit': self.bank_charges,
            'company_id': self.company_id.id,
            'is_bc_line': True
        }, {
            'account_id': self.journal_id.default_bank_charge_account_id.id,
            'partner_id': self.payment_type in ('inbound', 'outbound') and self.env['res.partner']._find_accounting_partner(self.partner_id).id or False,
            'name': _("Vendor Payment: %s" % self.ref),
            'debit': self.bank_charges,
            'company_id': self.company_id.id,
            'is_bc_line': True
        }]
        return charges

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        res = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
        if self.bank_charges > 0.0 and self.journal_id.default_bank_charge_account_id:
            res += self._create_bank_charges_entry()
        return res
