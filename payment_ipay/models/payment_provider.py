# -*- coding: utf-8 -*-
"""
Odoo Proprietary License v1.0.

see License:
https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html#odoo-apps
# Copyright ©2022 Bernard K. Too<bernard.too@optima.co.ke>
"""
import logging

from odoo import fields, models

LOGGER = logging.getLogger(__name__)


class Ipayprovider(models.Model):
    """Add ipay fields and methods."""

    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("ipayafrica", "iPay Payment Gateway")],
        ondelete={"ipayafrica": "set default"},
    )
    ipay_currency_id = fields.Many2one(
        "res.currency",
        "ipay Currency",
        required_if_provider="ipayafrica",
        default=lambda self: self.env.ref("base.KES").id,
        help="The ipay currency. Default is KES. \
                If the sales order is in a different currency other than the ipay currency, \
                it has to be converted to the ipay currency",
    )

    ipay_vendor_id = fields.Char(
        "Vendor ID", required_if_provider="ipayafrica", default="demo"
    )
    ipay_checkout_url = fields.Char(
        "Checkout URL",
        required_if_provider="ipayafrica",
        default="https://payments.ipayafrica.com/v3/ke",
    )
    ipay_callback_url = fields.Char(
        "Callback URL",
        required_if_provider="ipayafrica",
        default=lambda self: self.env["ir.config_parameter"].get_param(
            "web.base.url", ""
        )
        + "/payment/ipayafrica",
    )
    ipay_hash_key = fields.Char(
        "Hash Key", required_if_provider="ipayafrica", default="demoCHANGED"
    )
