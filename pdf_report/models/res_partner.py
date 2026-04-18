from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    eori_number = fields.Char(string='EORI Number', index=True)
    company_reg_number = fields.Char(string='Company Reg Number', index=True)

    # https://spantech.odoo.com/web#id=857&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    requirement = fields.Text("Customer Special Requirements", groups="sales_team.group_sale_manager")
