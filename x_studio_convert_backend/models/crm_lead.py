from odoo import fields, models, api


class CRMLead(models.Model):
    _inherit = "crm.lead"

    x_studio_area = fields.Char(string="Area")
    x_studio_percent_funds = fields.Integer(string="Percent Funds", default=100)
    x_studio_percent_mml = fields.Integer(string="Percentage Chance of Completion")
