from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TemplateAction(models.Model):
    _name = 'template.action'
    _description = 'Template Action'


    def _get_default_menu_action_ids(self):
        menu_actions = self.env['ir.ui.menu'].search([
            ('action', 'like', 'ir.actions.act_window'),
            ('name', 'in', ['Quotations', 'Orders', 'Requests for Quotation', 'Purchase Orders', 'Transfers', 'Invoices', 'Credit Notes'])
        ]).mapped('action')
        
        action_lst = [manu.id for manu in menu_actions]
        
        return [(6, 0, action_lst)]


    company_id = fields.Many2one(
            'res.company',
            string='Company',
            required=True
    )
    template_model = fields.Char(
        related="action_id.res_model",
        string="Model",
        store=True
    )
    email_template_id = fields.Many2one(
        'mail.template',
        string='Email Template'
    )
    pdf_report_id = fields.Many2one(
        'ir.actions.report',
        string='PDF Report'
    )
    active = fields.Boolean("Active", default=True)

    action_id = fields.Many2one(
        'ir.actions.act_window', 
        string="Action",
        domain="[('id', 'in', menu_action_ids)]"
    )
    
    menu_action_ids = fields.Many2many(
            'ir.actions.act_window',
            string='Menu Actions',
            default=_get_default_menu_action_ids
    )

    @api.constrains('company_id', 'action_id')
    def _check_unique_company_action(self):
        for record in self:
            existing_record = self.search([
                ('company_id', '=', record.company_id.id),
                ('action_id', '=', record.action_id.id),
                ('id', '!=', record.id)
            ], limit=1)

            if existing_record:
                raise ValidationError('This Action is already linked to the same company.')



    @api.onchange('pdf_report_id')
    def onchange_pdf_report_id(self):
        if self.pdf_report_id and self.email_template_id:
            self.email_template_id.report_template = self.pdf_report_id.id
    
    @api.onchange('email_template_id')
    def onchange_email_template_id(self):
        self.pdf_report_id = False
            