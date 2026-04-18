from odoo import fields, models, api


class CRMLead(models.Model):
    _inherit = "crm.lead"

    # https://spantech.odoo.com/web#id=467&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
    competition = fields.Char(string="Competition")
    scotsman_estimate = fields.Integer(string="Scotsman Estimate", compute='_compute_scotsman_estimate')
    # partner_responsible_rep = fields.Many2one(related="partner_id.partner_responsible_rep", string='Responsible Rep',
    #                                           tracking=True, readonly=False)
    partner_responsible_rep = fields.Many2one('res.partner', string='Responsible Rep', tracking=True)

    def _compute_scotsman_estimate(self):
        """
        Use:
        Added by: Jignesh
        Added on: 16/9/22
        Task: https://spantech.odoo.com/web#menu_id=554&cids=1%2C2%2C3%2C4&id=481&action=806&model=project.task&view_type=form
        """
        for crm in self:
            crm.scotsman_estimate = (crm.x_studio_percent_funds * crm.x_studio_percent_mml) / 100

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id and self.partner_id.partner_responsible_rep:
            self.partner_responsible_rep = self.partner_id.partner_responsible_rep.id
