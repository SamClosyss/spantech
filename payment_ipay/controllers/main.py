# -*- coding: utf-8 -*-
"""
Odoo Proprietary License v1.0.

see License:
https://www.odoo.com/documentation/user/15.0/legal/licenses/licenses.html#odoo-apps
# Copyright ©2023 Bernard K. Too<bernard.too@optima.co.ke>
"""
import logging

from odoo import _, http
from odoo.http import request

LOGGER = logging.getLogger(__name__)


class LipaNaiPay(http.Controller):
    """ iPay http routes for callback url and for submitting payment form data """

    @http.route(
        "/payment/ipayafrica", type="http", auth="public", methods=["GET"], website=True
    )
    def index(self, **params):
        """ Lina na iPay Callback URL data  handling"""
        LOGGER.info("Beginning iPay Africa Callback processing with data: %s", params)
        tx = (
            request.env["payment.transaction"]
            .sudo()
            ._get_tx_from_notification_data("ipayafrica", params)
        )
        if tx:
            tx._handle_notification_data("ipayafrica", params)
        else:
            msg = _(
                "IPAY_AFRICA: cannot find matching payment transaction.Redirecting to /shop/payment page."
            )
            LOGGER.warning(msg)
            return http.request.redirect("/shop/payment")
        return request.redirect("/payment/status")
