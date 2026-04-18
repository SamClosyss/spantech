from odoo import fields, models, api


class HREmployee(models.Model):
    _inherit = "hr.employee"

    # https://spantech.odoo.com/web?debug=1#id=746&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    national_health_insurance_number = fields.Char(string="National Health Insurance Number", groups="hr.group_hr_user",
                                                   tracking=True)
    social_security_number = fields.Char(string="Social Security Number (Kenya)", groups="hr.group_hr_user",
                                         tracking=True)
    kenyan_tax_pin = fields.Char(string="Kenyan Tax Pin", groups="hr.group_hr_user", tracking=True)
