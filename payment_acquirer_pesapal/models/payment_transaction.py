# -*- coding: utf-8 -*-
# Copyright (c) 2022-Present Mentis Consultancy Services. (<https://mcss.odoo.com>)

import base64
import logging
import json
import pprint
import requests
from werkzeug import urls

from odoo import _, models
from odoo.addons.payment import utils as payment_utils
from odoo.exceptions import ValidationError
from odoo.addons.payment_acquirer_pesapal.controllers.main import PesapalController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _retrieve_pesapal_payment(self, data):
        self.ensure_one()
        token = self._get_pespal_token()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token['token']
        }

        url = self.provider_id._get_pesapal_urls()
        res = requests.get(url + '/api/Transactions/GetTransactionStatus?orderTrackingId=%s' % data.get('OrderTrackingId'), headers=headers)
        return res.json()

    def _get_pespal_token(self):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "consumer_key": self.provider_id.pesapal_consumer_key,
            "consumer_secret": self.provider_id.pesapal_consumer_secret
        }

        url = self.provider_id._get_pesapal_urls()
        res = requests.post(url + '/api/Auth/RequestToken', data=json.dumps(data), headers=headers)

        if res.status_code != 200:
            raise ValidationError(_("Something went wrong to get pesapal token!\n%s" % pprint.pformat(res.text)))

        return res.json()

    def _register_pespal_ipn(self):
        token = self._get_pespal_token()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token['token']
        }

        base_url = self.provider_id.get_base_url()
        data = {
            "url": urls.url_join(base_url, PesapalController._ipn_url),
            "ipn_notification_type": "GET"
        }

        url = self.provider_id._get_pesapal_urls()
        res = requests.post(url + '/api/URLSetup/RegisterIPN', data=json.dumps(data), headers=headers)
        if res.status_code != 200:
            raise ValidationError(_("Something went wrong to register pesapal IPN!\n%s" % pprint.pformat(res.text)))

        return res.json()

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Pesapal-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of provider-specific processing values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'pesapal':
            return res

        base_url = self.provider_id.get_base_url()

        first_name, last_name = payment_utils.split_partner_name(self.partner_id.name)
        ipn_data = self._register_pespal_ipn()
        payload = {
            "id": self.reference,
            "currency": self.currency_id.name,
            "amount": self.amount,
            "description": self.reference,
            "callback_url": urls.url_join(base_url, PesapalController._callback_url),
            "notification_id": ipn_data['ipn_id'],
            "billing_address": {
                "email_address": self.partner_email,
                "phone_number": self.partner_phone,
                "country_code": self.partner_country_id.code,
                "first_name": first_name,
                "last_name": last_name,
                "line_1": self.partner_address,
                "city": self.partner_city,
                "zip_code": self.partner_zip
            }
        }

        url = self.provider_id._get_pesapal_urls()

        token = self._get_pespal_token()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token['token']
        }

        response = requests.request('POST', url + '/api/Transactions/SubmitOrderRequest', data=json.dumps(payload), headers=headers, timeout=160)

        if response.status_code != 200:
            if response.json().get('error'):
                raise ValidationError(response.json().get('error').get('message'))
            else:
                raise ValidationError(_("Something went wrong with the Pesapal!\n%s" % pprint.pformat(response.text)))

        resp = response.json()
        if resp.get('error'):
            raise ValidationError(resp['error']['message'])
        self.write({'provider_reference': resp['order_tracking_id']})
        res.update({'api_url': '/payment/pesapal/redirect?url=' + base64.b64encode(resp['redirect_url'].encode('UTF-8')).decode('UTF-8')})
        return res

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Pesapal data.

        :param str provider_code: The code of the provider that handled the transaction
        :param dict notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if inconsistent data were received
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'pesapal' or len(tx) == 1:
            return tx

        reference = notification_data.get('OrderMerchantReference')
        if not reference:
            raise ValidationError(
                "Pespal: " + _(
                    "Received data with missing reference %(r)s.",
                    r=reference
                )
            )

        tx = self.search([('reference', '=', reference), ('provider_code', '=', provider_code)])
        if not tx:
            raise ValidationError(
                "Pesapal: " + _("No transaction found matching reference %s." % reference)
            )

        return tx

    def _process_notification_data(self, notification_data):
        """ Override of `payment' to process the transaction based on Pesapal data.

        Note: self.ensure_one()

        :param dict notification_data: The notification data sent by the provider.
        :return: None
        :raise ValidationError: If inconsistent data are received.
        """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'pesapal':
            return

        notification_data.update(self._retrieve_pesapal_payment(notification_data))

        status = notification_data['status_code']

        if status == 1:
            _logger.info('Pesapal payment for tx %s: set as DONE' % (self.reference))
            self._set_done()
        elif status in [0, 2]:
            _logger.info('Pesapal payment for tx %s: set as CANCELLED' % (self.reference))
            self._set_canceled()
        else:
            msg = 'Received unrecognized response for Pesapal Payment %s, set as error' % (self.reference)
            _logger.info(msg)
            self.write({
                'state_message': msg
            })
            self._set_error(msg)
