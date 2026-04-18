# -*- coding: utf-8 -*-
# Copyright (c) 2022-Present Mentis Consultancy Services. (<https://mcss.odoo.com>)

import base64
import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class PesapalController(http.Controller):
    _callback_url = '/payment/pesapal/callback'
    _ipn_url = '/payment/pesapal/ipn'

    @http.route('/payment/pesapal/redirect', type='http', auth='public', csrf=False)
    def pesapal_redirect(self, **post):
        url = base64.b64decode(post.get('url'))
        return werkzeug.utils.redirect(url)

    @http.route([_callback_url, _ipn_url], type='http', auth='public', csrf=False, save_session=False)
    def pesapal_handle_feedback(self, **data):
        _logger.info('Pesapal: entering form_feedback with post data %s', pprint.pformat(data))
        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
            'pesapal', data
        )
        tx_sudo._handle_notification_data('pesapal', data)
        return request.redirect('/payment/status')
