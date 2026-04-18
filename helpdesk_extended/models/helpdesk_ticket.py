from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    # https://spantech.odoo.com/web?debug=1#id=749&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    historic_st_number = fields.Char(string="Historic ST Number")
    historic_date = fields.Char(string="Historic Date")
    work_order = fields.Char(string="Work Order")
    rma_number = fields.Char(string="RMA Number")
    status_spl = fields.Char(string="Status")
    arrival_date_at_spl = fields.Char(string="Arrival Date At SPL")
    shipping_date_to_service = fields.Char(string="Shipping Date To Service")
    product_serial_number = fields.Char(string="Product Serial Number")
    client_po = fields.Char(string="Client PO")
    invoiced_to_client_on = fields.Char(string="Invoiced To Client On")
    receipt = fields.Char(string="Receipt")
    # product_tmpl_id = fields.Many2one('product.template', 'Product Template', related='product_id.product_tmpl_id')
    # product_tmpl_id = fields.Many2one(related='product_id.product_tmpl_id', string='Product Template')

    # https://spantech.odoo.com/web?debug=1#id=1085&menu_id=554&cids=4%2C7%2C3%2C2%2C1%2C6%2C8%2C5%2C10%2C9&action=806&model=project.task&view_type=form
    organisation_id = fields.Many2one('res.partner', string='Organisation', tracking=True)

    @api.depends('partner_id')
    def _compute_suitable_product_ids(self):
        """
        Use: Add MML Instrument tag products in product selection
        Added by: Jignesh
        Added on: 26/4/23
        Task: https://spantech.odoo.com/web?debug=1#menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5%2C10%2C9&id=1027&action=806&model=project.task&view_type=form
        """
        super(HelpdeskTicket, self)._compute_suitable_product_ids()
        product_obj = self.env['product.product']
        for ticket in self.filtered(lambda t: t.company_id.report_format == 'MML_report'):
            mml_instrument_product_ids = product_obj.search([("product_tag_ids", "=", "MML Instrument")])
            if mml_instrument_product_ids:
                ticket.suitable_product_ids += mml_instrument_product_ids


    def message_subscribe(self, partner_ids=None, subtype_ids=None):
        res = super(HelpdeskTicket, self).message_subscribe(partner_ids=partner_ids, subtype_ids=subtype_ids)
        _logger.info("\n\n Partner ids: %s", partner_ids)

        restrict_ids = set(self.team_id.restrict_partner_ids.ids)
        current_partner_ids = set(partner_ids or [])
        existing_follower_ids = set(self.message_partner_ids.ids)

        # Combine and find restricted partners to remove
        partners_to_remove = list((current_partner_ids | existing_follower_ids) & restrict_ids)

        if partners_to_remove:
            self.message_unsubscribe(partner_ids=partners_to_remove)
        return res

    def message_post(self, **kwargs):
        res = super(HelpdeskTicket, self).message_post(**kwargs)
        if self.team_id and self.team_id.restrict_partner_ids:
            self.message_unsubscribe(partner_ids=self.team_id.restrict_partner_ids.ids)
        return res

    def _notify_get_reply_to(self, default=None):
        """
        Override to prevent internal users from setting the team alias as reply-to.
        """
        # If current user is internal, don't return reply-to for any ticket
        if self.env.user.has_group('base.group_user'):
            _logger.info(
                    "[HelpdeskTicket] Reply-to skipped for internal user (ID: %s, Login: %s)",
                    self.env.user.id, self.env.user.login
                    )
            return {ticket.id: False for ticket in self}

        # Otherwise, proceed with the original enterprise behavior
        aliases = self.mapped('team_id').sudo()._notify_get_reply_to(default=default)
        _logger.debug("[HelpdeskTicket] Retrieved team aliases: %s", aliases)
        res = {ticket.id: aliases.get(ticket.team_id.id) for ticket in self}
        leftover = self.filtered(lambda rec: not rec.team_id)
        _logger.info(
                "[HelpdeskTicket] Tickets without team found: %s",
                leftover.ids
                )
        if leftover:
            res.update(super(HelpdeskTicket, leftover)._notify_get_reply_to(default=default))
        return res
