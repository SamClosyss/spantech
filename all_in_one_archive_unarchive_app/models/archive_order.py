# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    active = fields.Boolean('Active', default=True)


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    active = fields.Boolean('Active', default=True)


class Inventory(models.Model):
    _inherit = "stock.picking"

    active = fields.Boolean('Active', default=True)


class Invoice(models.Model):
    _inherit = "account.move"

    active = fields.Boolean('Active', default=True)


class Payment(models.Model):
    _inherit = "account.payment"

    active = fields.Boolean('Active', default=True)
