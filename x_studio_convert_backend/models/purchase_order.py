from odoo import api, fields, models

PURCHASE_FOR = [('purchased for stock', 'Purchased For Stock'),
                ('WIP', 'Purchased For Work In Progress')]

CREDIT_CARD = [('Andy Bird Credit card', 'Andy Bird Credit card'),
               ('BW Credit card', 'BW Credit card'),
               ('JH Credit card', 'JH Credit card'),
               ('LS Credit card', 'LS Credit card'),
               ('PG Credit card', 'PG Credit card'),
               ('AH Credit card', 'AH Credit card'),
               ('Ben Beake Credit card', 'Ben Beake Credit card'),
               ('Josh Roberts Credit card', 'Josh Roberts Credit card'),
               ('Nick Pickford Credit card', 'Nick Pickford Credit card'),
               ('Paul Cooper Credit card', 'Paul Cooper Credit card'),
               ('Richard Thompson Credit card', 'Richard Thompson Credit card'),
               ('Krish Narain Credit card', 'Krish Narain Credit card')]


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_studio_char_field_tfa4O = fields.Char(string='Purchase order sent by')
    x_studio_r_d_expense = fields.Boolean(string="R & D Expense")
    x_studio_selection_field_KBmMT = fields.Selection(PURCHASE_FOR, string="Purchased for?")
    x_studio_selection_field_v8tWq = fields.Selection(CREDIT_CARD, string="Credit card used?")
