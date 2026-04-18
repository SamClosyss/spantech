# ©  2008-2021 Deltatech
# See README.rst file on addons root folder for license details

import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class RevolutController(http.Controller):
    @http.route("/payment/revolut/return", type="json", auth="public")
    def revolut_return(self, post):
        _logger.info("Beginning Revolut return form_feedback with post data %s", str(post))  # debug
        if post:
            request.env["payment.transaction"].sudo()._handle_notification_data("revolut", post)
