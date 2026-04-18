from odoo import api, fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    active = fields.Boolean('Active', default=True)

class ProjectProject(models.Model):
    _inherit = 'project.project'

    x_studio_project_code = fields.Integer(string="Project Code")
