# ©  2015-2021 Deltatech
# See README.rst file on addons root folder for license details


import json
import logging

import requests

from odoo import _, api, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _get_specific_processing_values(self, processing_values):
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != "revolut":
            return res
        data = dict()

        if self.provider_id.capture_manually:
            capture_mode = "MANUAL"
        else:
            capture_mode = "AUTOMATIC"

        url = self.provider_id._revolut_get_api_url() + "/orders"
        json_param = {
            "amount": processing_values["amount"] * 100,
            "currency": self.currency_id.name,
            "capture_mode": capture_mode,
            "email": self.partner_id.email,
            "name": self.partner_id.name,
        }
        if not self.provider_id.revolut_api_key:
            raise UserError(_("Missing API Key"))

        headers = {"Authorization": "Bearer " + self.provider_id.revolut_api_key}

        req = requests.post(url, json=json_param, headers=headers, timeout=30)

        _logger.info(req.content)
        req.raise_for_status()
        if "json" in req.headers["Content-Type"]:
            data = json.loads(req.content)

        self.write({"provider_reference": data.get("id")})

        if self.provider_id.state == "enabled":
            data["environment"] = "prod"
        else:
            data["environment"] = "sandbox"
        return data

    # def _get_specific_rendering_values(self, processing_values):
    #     res = super()._get_specific_rendering_values(processing_values)
    #     if self.provider != "revolut":
    #         return res
    #
    #     url = self.provider_id._revolut_get_api_url() + "/orders"
    #     json_param = {
    #         "amount": processing_values["amount"],
    #         "currency": self.currency_id.name,
    #     }
    #     headers = {"Authorization": "Bearer " + self.provider_id.revolut_api_key}
    #
    #     req = requests.post(url, json=json_param, headers=headers)
    #
    #     _logger.info(req.content)
    #     req.raise_for_status()
    #     if "json" in req.headers["Content-Type"]:
    #         data = json.loads(req.content)
    #         processing_values.update(data)
    #
    #     # processing_values["api_url"] = "#"
    #
    #     return processing_values

    @api.model
    def _get_tx_from_notification_data(self, provider_code, data):
        tx = super()._get_tx_from_notification_data(provider_code, data)
        if provider_code != "revolut":
            return tx
        reference = data.get("reference")
        tx = self.search([("reference", "=", reference), ("provider_code", "=", "revolut")])
        if not tx:
            raise ValidationError(_("No transaction found matching reference %s.", reference))
        return tx

    def _process_notification_data(self, data):
        super()._process_notification_data(data)
        if self.provider_code != "revolut":
            return
        _logger.info("revolut form validate with post data %s", str(data))

        return self._revolut_get_status(data.get("id"))

    def _revolut_get_status(self, order_id):
        url = self.provider_id._revolut_get_api_url() + "/orders/" + order_id
        headers = {"Authorization": "Bearer " + self.provider_id.revolut_api_key}

        req = requests.get(url, headers=headers, timeout=30)
        _logger.info(req.content)
        req.raise_for_status()
        data = dict()
        if "json" in req.headers["Content-Type"]:
            data = json.loads(req.content)

        state = data.get("state")
        # Enum: "PENDING" "PROCESSING" "AUTHORISED" "COMPLETED" "CANCELLED" "FAILED"
        if state == "PENDING":
            self._set_pending()
        elif state == "AUTHORISED":
            self._set_authorized()
        elif state == "COMPLETED":
            self._set_done()
        elif state == "CANCELLED":
            self._set_canceled()
        elif state == "FAILED":
            self._set_error("error")
            return False

        return True

    def _send_capture_request(self):
        super()._send_capture_request()
        if self.provider_code != "revolut":
            return
        _logger.info("revolut _send_capture_request")

        order_id = self.provider_reference
        url = self.provider_id._revolut_get_api_url() + "/orders/" + order_id + "/capture"
        headers = {"Authorization": "Bearer " + self.provider_id.revolut_api_key}
        json_param = {
            "amount": self.amount * 100,
        }
        req = requests.post(url, json=json_param, headers=headers, timeout=30)

        _logger.info(req.content)
        req.raise_for_status()

        self._revolut_get_status(order_id)

    def _send_void_request(self):
        super()._send_void_request()
        if self.provider_code != "revolut":
            return
        _logger.info("revolut _send_void_request")

        order_id = self.provider_reference
        url = self.provider_id._revolut_get_api_url() + "/orders/" + order_id + "/cancel"
        headers = {"Authorization": "Bearer " + self.provider_id.revolut_api_key}
        json_param = {
            "amount": self.amount * 100,
        }
        req = requests.post(url, json=json_param, headers=headers, timeout=30)

        _logger.info(req.content)
        req.raise_for_status()
        self._revolut_get_status(order_id)
