from odoo import api, models, fields


class MailInvite(models.TransientModel):
    _inherit = 'mail.wizard.invite'


    def _domain_partner_ids(self):
        domain = [('type', '!=', 'private')]
        print("context-----------------------",self._context)
        res_model = self._context.get('default_res_model')
        res_id = self._context.get('default_res_id')
        if res_model == 'helpdesk.ticket' and res_id:
            document = self.env[res_model].browse(res_id)
            excluded_partner_ids = document.team_id.message_follower_ids.mapped('partner_id').ids
            domain += [('id', 'not in', excluded_partner_ids)]
            print("domain--------------------------------------", domain)
        return domain

    # Overwrite partner field to add domain
    partner_ids = fields.Many2many('res.partner', string='Recipients', help="List of partners that will be added as follower of the current document.",
                                   domain=_domain_partner_ids)

