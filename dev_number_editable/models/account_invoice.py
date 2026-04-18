# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api, _

class account_invoice(models.Model):
    _inherit = 'account.move'

    
    cop_name = fields.Char(string='data',compute='get_user_access')
    
    
    @api.depends('name')
    def get_user_access(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        for data in self:
            if res_user.has_group('dev_number_editable.group_number_edit'):
                data.cop_name = True
            else:
                data.cop_name = False
        
        
        
