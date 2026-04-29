from odoo import api, models,fields


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    refund_method = fields.Selection(selection=[
        ('refund', 'Partial Refund'),
        ('cancel', 'Full Refund'),
        ('modify', 'Full refund and new draft invoice')
    ], string='Credit Method', required=True,
        help='Choose how you want to credit this invoice. You cannot "modify" nor "cancel" if the invoice is already reconciled.')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        if not self.env.company.x_use_ti:
            return res

        move_ids = self.env['account.move']

        # noinspection PyUnresolvedReferences
        if self.env.context.get('active_model') == 'helpdesk.ticket' and 'move_id' in self.env.context:
            # handle call from helpdesk module
            move_ids = move_ids.browse(self.env.context['move_id'])
            res['move_ids'] = [(6, 0, move_ids.ids)]

        return res

    def _prepare_default_reversal(self, move):
        result = super()._prepare_default_reversal(move=move)
        # reverse_date = self.date if self.date_mode == 'custom' else move.date

        if self.env.company.x_use_ti:
            result.update({'ref': self.reason, 'partner_bank_id': move.partner_bank_id.id})

        return result

    def reverse_moves(self):
        self.ensure_one()

        if self.env.company.x_use_ti:
            if self.refund_method == 'refund':
                self = self.with_context(check_move_validity=False)

        return super().reverse_moves()
