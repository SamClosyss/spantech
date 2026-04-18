from odoo import api, models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_confirmation_sent = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='ICS', readonly=True,
                                                 copy=False, index=True, default='no', help="Invoice Confirmation Sent")

    # https://spantech.odoo.com/web?debug=1#id=331&cids=1%2C2%2C3%2C4&menu_id=554&action=806&model=project.task&view_type=form
    note = fields.Html(string='Comment')

    @api.depends('restrict_mode_hash_table', 'state')
    def _compute_show_reset_to_draft_button(self):
        # Add same methd for testing due to some customer vendor bills not display reset to draft button on live db
        super(AccountMove, self)._compute_show_reset_to_draft_button()
        for move in self:
            move.show_reset_to_draft_button = not move.restrict_mode_hash_table and move.state in ('posted', 'cancel')
