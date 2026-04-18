from odoo import fields, api, models, _
from lxml import etree


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    def action_rfq_send(self):
        res = super(PurchaseOrder, self).action_rfq_send()
        action_id = False
        if self.state in ('purchase','done'):
            action_id = self.env.ref('purchase.purchase_form_action').id
        if self.state not in ('purchase','done'):
            action_id = self.env.ref('purchase.purchase_rfq').id
        template_action = self.env['template.action'].search([
        ('action_id', '=', action_id),
        ('company_id', '=', self.company_id.id),
        ('active', '=', True)
        ], limit=1)
        if template_action.id and template_action.email_template_id.id:
            template_id = template_action.email_template_id.id
            res['context'].update({'default_template_id': template_id})
            mail_compose = self.env['mail.compose.message'].search([
                ('model', '=', 'purchase.order'),
                ('template_id', '=', template_id)
            ], limit=1)
            if mail_compose:
                mail_compose.template_id.report_template = template_action.pdf_report_id.id
        return res

    def print_quotation(self):
        self.write({'state': "sent"})
        action_id = False
        if self.state in ('purchase','done'):
            action_id = self.env.ref('purchase.purchase_form_action').id
        if self.state not in ('purchase','done'):
            action_id = self.env.ref('purchase.purchase_rfq').id
        template_action = self.env['template.action'].search([
        ('action_id', '=', action_id),
        ('company_id', '=', self.company_id.id),
        ('active', '=', True)
        ], limit=1)
        if template_action.id:
            report = self.env['ir.actions.report'].search([('name', '=', template_action.pdf_report_id.name)], limit=1)
            report_xmlid = self.env['ir.model.data'].search([('model', '=', 'ir.actions.report'), ('res_id', '=', report.id)])
            return self.env.ref(report_xmlid.complete_name).report_action(self)
        return self.env.ref('purchase.report_purchase_quotation').report_action(self)


class Picking(models.Model):
    _inherit = 'stock.picking'

    def do_print_picking(self):
        self.write({'printed': True})
        action_id = False
        if self.state == 'assigned':
            action_id = self.env.ref('stock.action_picking_tree_all').id
        template_action = self.env['template.action'].search([
        ('action_id', '=', action_id),
        ('company_id', '=', self.company_id.id),
        ('active', '=', True)
        ], limit=1)
        if template_action.id:
            report = self.env['ir.actions.report'].search([('name', '=', template_action.pdf_report_id.name)], limit=1)
            report_xmlid = self.env['ir.model.data'].search([('model', '=', 'ir.actions.report'), ('res_id', '=', report.id)])
            return self.env.ref(report_xmlid.complete_name).report_action(self)
        return self.env.ref('stock.action_report_picking').report_action(self)