# -*- coding: utf-8 -*-
"""
Odoo Proprietary License v1.0.

see License:
https://www.odoo.com/documentation/user/15.0/legal/licenses/licenses.html#odoo-apps
# Copyright ©2022 Bernard K. Too<bernard.too@optima.co.ke>
"""
import logging

from odoo import _, api, fields, models

LOGGER = logging.getLogger(__name__)


class Paymentipay(models.Model):
    """Create iPay related methods and fields."""

    _name = "ipay.data"
    _description = "iPay Payment Gateway Data"
    _order = "id desc"

    qwh = fields.Char()
    afd = fields.Char()
    poi = fields.Char()
    uyt = fields.Char()
    ifd = fields.Char()
    agt = fields.Char()
    p1 = fields.Char()
    p2 = fields.Char()
    p3 = fields.Char()
    p4 = fields.Char()
    order_id = fields.Char("Order Ref")
    mc = fields.Monetary("Amount Paid", currency_field="currency_id")
    currency_id = fields.Many2one(
        "res.currency", "Currency", default=lambda self: self.env.ref("base.KES").id
    )
    txncd = fields.Char("Transaction Code")
    status = fields.Char("Status")
    ivm = fields.Char("Invoice ID")
    msisdn_id = fields.Char("Customer ID")
    msisdn_idnum = fields.Char("Customer Phone")
    channel = fields.Char("Payment Channel")
    tokenid = fields.Char("Token ID")
    tokenemail = fields.Char("Token Email")
    card_mask = fields.Char("Card Mask")
    reconciled = fields.Boolean("Reconciled", default=False)
    provider_id = fields.Many2one("payment.provider", "Payment Gateway")

    @api.depends("msisdn_id", "txncd")
    def name_get(self):
        """Change the default naming of ipay transactions in Odoo."""
        res = []
        for rec in self:
            name = (rec.msisdn_id or "") + " / " + (rec.txncd or "")
            res.append((rec.id, name))
        return res

    @api.model
    def save_data(self, params):
        """Store the payment data for ipay Payment Gateway."""
        if params:
            if params.get("id"):
                params["order_id"] = params.get("id")
                params.pop("id")
            params.update(
                reconciled=False,
            )
            return self.create(params)
        msg = _("IPAY_AFRICA: Payment data received was not saved.")
        LOGGER.warning(msg)
        return False
