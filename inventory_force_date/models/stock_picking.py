# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import date, datetime, time, timedelta
from odoo.fields import Date, Datetime
from odoo.tools import float_compare


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    force_inventory_date = fields.Datetime(string="Force Inventory Date", required=False, )

