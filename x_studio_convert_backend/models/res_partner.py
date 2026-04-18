from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    x_studio_many2one_field_5MK2F = fields.Many2one('account.incoterms', string='Incoterm')
    x_studio_contact_name = fields.Char(string="Contact Name")
    x_studio_contact_telephone_number = fields.Char(string="Contact Telephone Number")
    x_studio_erpag_account_number = fields.Char(string="Internal Account Number")

    # https://spantech.odoo.com/web?debug=1#menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5%2C10%2C9&id=1027&action=806&model=project.task&view_type=form
    mml_product_info_ids = fields.Many2many('product.template', compute='_compute_mml_product_info_ids',
                                            string='Related MML Products')

    def _compute_mml_product_info_ids(self):
        """
        Use: Linked the products (MML Instruments) to the selected customer (Owner) of the MML tab
        Added by: Jignesh
        Added on: 26/4/23
        Task: https://spantech.odoo.com/web?debug=1#menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5%2C10%2C9&id=1027&action=806&model=project.task&view_type=form
        """
        for partner in self:
            product_ids = self.env['product.product'].search([('mml_owner', '=', partner.id)])
            partner.mml_product_info_ids = product_ids and product_ids.mapped('product_tmpl_id') or False

    @api.model_create_multi
    def create(self, vals):
        """
        Use: prevention of changes to customer information
        Added by: Jignesh
        Added on: 6/1/23
        Task: https://spantech.odoo.com/web?debug=1#id=790&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
        """
        if not self.env.is_admin():
            raise UserError(_("You don't have the rights to create partner. Please contact an Administrator."))
        else:
            return super(ResPartner, self).create(vals)

    def write(self, vals):
        """
        Use: prevention of changes to customer information
        Added by: Jignesh
        Added on: 6/1/23
        Task: https://spantech.odoo.com/web?debug=1#id=790&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
        """
        if not self.env.is_admin():
            raise UserError(_("You don't have the rights to write partner. Please contact an Administrator."))
        else:
            return super(ResPartner, self).write(vals)

    def unlink(self):
        """
        Use: prevention of changes to customer information
        Added by: Jignesh
        Added on: 6/1/23
        Task: https://spantech.odoo.com/web?debug=1#id=790&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
        """
        if not self.env.is_admin():
            raise UserError(_("You don't have the rights to unlink partner. Please contact an Administrator."))
        else:
            return super(ResPartner, self).unlink()


class ResUsers(models.Model):
    _inherit = "res.users"

    x_studio_many2one_field_5MK2F = fields.Many2one(related="partner_id.x_studio_many2one_field_5MK2F",
                                                    string="Incoterm")
    x_studio_contact_name = fields.Char(related="partner_id.x_studio_contact_name", string="Contact Name")
    x_studio_contact_telephone_number = fields.Char(related="partner_id.x_studio_contact_telephone_number",
                                                    string="Contact Telephone Number")
    x_studio_erpag_account_number = fields.Char(related="partner_id.x_studio_erpag_account_number",
                                                string="Internal Account Number")
