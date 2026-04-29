from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # ticket_count = fields.Integer(string='Ticket Count', compute='_compute_ticket_count')
    # ticket_ids = fields.One2many('helpdesk.ticket', 'product_tmpl_id', string='Helpdesk Ticket')
    #
    # @api.depends('ticket_ids')
    # def _compute_ticket_count(self):
    #     self.ticket_count = len(self.ticket_ids)

    def action_view_tickets(self):
        action = self.env["ir.actions.actions"]._for_xml_id("helpdesk.helpdesk_ticket_action_main_my")
        action['domain'] = [('product_id', 'in', self.product_variant_ids.ids)]
        action['display_name'] = _("Helpdesk Tickets for %s", self.display_name)
        return action
