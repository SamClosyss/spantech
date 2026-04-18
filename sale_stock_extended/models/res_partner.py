from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_IGM_customer = fields.Boolean("Is Requires in IGM")
    is_delivery_notify = fields.Boolean("Notify Delivery Update")

    # https://spantech.odoo.com/web#id=1153&menu_id=554&cids=4%2C1%2C7%2C3%2C8%2C6%2C5%2C10%2C9%2C2&action=806&model=project.task&view_type=form
    # TODO: override bedloe field and set default as True
    use_partner_credit_limit = fields.Boolean(
        string='Partner Limit', groups='account.group_account_invoice,account.group_account_readonly',
        compute='_compute_use_partner_credit_limit', inverse='_inverse_use_partner_credit_limit', default=True)
    partner_limit_default = fields.Boolean("Partner Limit Default", default=True, copy=False)

    # https://spantech.odoo.com/web?debug=1#menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5&id=921&action=806&model=project.task&view_type=form
    partner_responsible_rep = fields.Many2one('res.partner', string='Responsible Rep', tracking=True)

    @api.model
    def default_get(self, fields):
        """
        Use: make the use partner limit Default
        Added by: Jignesh
        Added on: 10/8/23
        Task: https://spantech.odoo.com/web#id=1153&menu_id=554&cids=4%2C1%2C7%2C3%2C8%2C6%2C5%2C10%2C9%2C2&action=806&model=project.task&view_type=form
        """
        res = super(ResPartner, self).default_get(fields)
        res['property_payment_term_id'] = False
        res['partner_limit_default'] = True
        return res


    @api.depends_context('company')
    def _compute_use_partner_credit_limit(self):
        """
        Use: make the use partner limit Default
        Added by: Jignesh
        Added on: 10/8/23
        Task: https://spantech.odoo.com/web#id=1153&menu_id=554&cids=4%2C1%2C7%2C3%2C8%2C6%2C5%2C10%2C9%2C2&action=806&model=project.task&view_type=form
        """
        for partner in self:
            company_limit = self.env['ir.property']._get('credit_limit', 'res.partner')
            # partner.use_partner_credit_limit = partner.credit_limit != company_limit
            if partner.partner_limit_default:
                partner.use_partner_credit_limit = True
            else:
                partner.use_partner_credit_limit = partner.credit_limit != company_limit
            # partner.use_partner_credit_limit = True if company_limit <= 0.0 else partner.credit_limit != company_limit

    def _inverse_use_partner_credit_limit(self):
        """
        Use: make the use partner limit Default
        Added by: Jignesh
        Added on: 10/8/23
        Task: https://spantech.odoo.com/web#id=1153&menu_id=554&cids=4%2C1%2C7%2C3%2C8%2C6%2C5%2C10%2C9%2C2&action=806&model=project.task&view_type=form
        """
        for partner in self:
            if not partner.use_partner_credit_limit:
                partner.credit_limit = self.env['ir.property']._get('credit_limit', 'res.partner')
                partner.partner_limit_default = False
