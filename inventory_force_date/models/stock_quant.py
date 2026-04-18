# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare


class Inventory(models.Model):
    _inherit = 'stock.quant'

    force_inventory_date = fields.Datetime(string="Force Inventory Date", required=False, )

    @api.model
    def _get_forbidden_fields_write(self):
        """ Returns a list of fields user can't edit when he want to edit a quant in `inventory_mode`."""
        return ['product_id', 'location_id', 'package_id', 'owner_id']

    def _get_inventory_move_values(self, qty, location_id, location_dest_id, out=False):
        res = super(Inventory, self)._get_inventory_move_values(qty, location_id, location_dest_id, out)
        if self.force_inventory_date and self.env.user.has_group("inventory_force_date.group_force_inventory_date"):
            res.update({
                'force_inventory_date': self.force_inventory_date
            })
        return res

    def action_apply_inventory(self):
        super(Inventory, self).action_apply_inventory()
        for quant in self:
            quant.force_inventory_date = False

    @api.model
    def _get_inventory_fields_write(self):
        fields = super(Inventory, self)._get_inventory_fields_write()
        fields += ['force_inventory_date']
        return fields

    def action_set_inventory_quantity_to_zero(self):
        super(Inventory, self).action_set_inventory_quantity_to_zero()
        self.action_reset_force_inventory_date()

    def action_reset_force_inventory_date(self):
        self.force_inventory_date = False
