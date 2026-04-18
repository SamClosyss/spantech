from odoo import fields, models, api


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"


    restrict_partner_ids = fields.Many2many('res.partner', 'helpdesk_team_restrict_partner_rel', 'helpdesk_team_id',
                                            'restrict_partner_id', string="Restrict Partner")
