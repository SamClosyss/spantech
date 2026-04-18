# -*- coding: utf-8 -*-

from odoo import fields, models

class BaseLanguageImport(models.TransientModel):

    _inherit = "base.language.import"

    code = fields.Char(size=None)