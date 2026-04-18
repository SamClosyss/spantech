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

class sale_order(models.Model):
    _inherit = 'sale.order'

    
    cop_name = fields.Char(string='data',compute='get_user_access')
    name = fields.Char(string='Order Reference', required=True, copy=False, index=True, default=lambda self: _('New'),)
    
    
    @api.depends('name')
    def get_user_access(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        self.cop_name = False
        for data in self:
            if res_user.has_group('dev_number_editable.group_number_edit'):
                data.cop_name = True
               
        
        
        
