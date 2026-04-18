from odoo import fields, models, api


class HRExpense(models.Model):
    _inherit = "hr.expense"

    x_studio_expense_relating_to_r_d = fields.Boolean("	R & D Expense")
