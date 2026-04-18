from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    gtm_container_key = fields.Char(string='Container ID')
