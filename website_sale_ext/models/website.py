# -*- coding: utf-8 -*-

from odoo import fields, models,api, _
from odoo.tools.translate import html_translate


class Website(models.Model):
    _inherit = "website"

    show_line_subtotals_tax_selection = fields.Selection(
        selection=[
            ('tax_excluded', "Tax Excluded"),
            ('tax_included', "Tax Included"),
        ],
        string="Line Subtotals Tax Display",
        required=True, default='tax_excluded',
    )

    @api.model
    def _get_default_error_msg(self):
        return '''
            <div>
                <h4>
                    Sorry, we are unable to ship your order
                </h4>
                <p>
                    No shipping method is available for your current order and shipping address. Please contact us for more information.
                </p>
            </div> '''

    custom_error_message = fields.Boolean('Custom Error Message')
    payment_error_message = fields.Html('Error Message', default=_get_default_error_msg)
    stock_in_custom_msg = fields.Boolean('Show Stock in custom Message')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_id = fields.Many2one(
        'website',
        string="website",
        ondelete='cascade'
    )
    show_line_subtotals_tax_selection = fields.Selection(
        readonly=False,
    )


    # @api.onchange('website_id')
    # def onchange_website_id(self):
    #     if self.website_id:
    #         self.show_line_subtotals_tax_selection = self.website_id.show_line_subtotals_tax_selection

    def set_values(self):
        super().set_values()
        # install a chart of accounts for the given company (if required)
        if self.env.company == self.company_id \
                and self.chart_template_id \
                and self.chart_template_id != self.company_id.chart_template_id:
            self.chart_template_id._load(self.env.company)
        # if self.show_line_subtotals_tax_selection:
        #     self.website_id.show_line_subtotals_tax_selection = self.show_line_subtotals_tax_selection
        
        sequence = 1
        if self.website_id:
            self.website_id.sequence = sequence
            website_ids = self.env['website'].search([('company_id', '=', self.website_id.company_id.id)])
            for website in website_ids:
                if self.website_id.id != website.id:
                    website.sequence += sequence
                
