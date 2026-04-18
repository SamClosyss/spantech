from odoo import fields, models, api


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    @api.constrains('use_website_helpdesk_form', 'privacy_visibility')
    def _check_website_privacy(self):
        if any(t.use_website_helpdesk_form and t.privacy_visibility != 'portal' for t in self):
            # raise ValidationError(_(
            #     'The visibility of the team needs to be set as "Invited portal users and all internal users" in order to use the website form.'))
            return True
