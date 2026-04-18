from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    notify_picking_ids = fields.Many2many('stock.picking', compute='_compute_notify_picking_ids')

    def _compute_notify_picking_ids(self):
        for r in self:
            r.notify_picking_ids = False
            domain = [('state', '=', 'assigned'), ('picking_type_code', '=', 'outgoing'),
                      ('company_id.report_format', '=', 'MML_report')]
            r.notify_picking_ids = self.env['stock.picking'].search(domain)

    @api.model
    def send_weekly_stock_notification(self):
        company = self.search([('report_format', '=', 'MML_report')])
        notify_partner_ids = self.env['res.partner'].search([('is_delivery_notify', '=',True)])
        if company and notify_partner_ids:
            mail_template = self.env.ref('sale_stock_extended.mail_template_send_weekly_delivery_notification',
                                         raise_if_not_found=False)
            if not mail_template:
                _logger.warning(
                    "The mail template with xmlid mail_template_send_weekly_delivery_notification has been deleted."
                )
            else:
                emails = {partner.email for partner in notify_partner_ids}
                print(company.notify_picking_ids.mapped('move_ids_without_package'))
                print(company.notify_picking_ids)
                mail_template.with_context(**{
                    'email_to': ','.join(emails),
                    'move_ref': company.notify_picking_ids.mapped('move_ids_without_package'),
                }).send_mail(company.id)
