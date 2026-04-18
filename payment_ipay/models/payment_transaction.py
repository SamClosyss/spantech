# -*- coding: utf-8 -*-
"""
Odoo Proprietary License v1.0.

see License:
https://www.odoo.com/documentation/user/15.0/legal/licenses/licenses.html#odoo-apps
# Copyright ©2022 Bernard K. Too<bernard.too@optima.co.ke>
"""
import hashlib
import hmac
import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

LOGGER = logging.getLogger(__name__)

FIELDS = "live.reference.amount.partner_phone.partner_email.vendor.currency_name.callback_url.crl"
# if paid exact or more (valid)
SUCCESS = ["aei7p7yrx4ae34", "eq3i7p5yt7645e"]
# if txn invalid or already used code
FAILED = ["fe2707etr5s4wq", "cr5i3pgy9867e1"]
# if paid less or txn pending
PENDING = ["bdi6p2yy76etrs", "dtfi4p7yty45wq"]


class IpayTransaction(models.Model):
    """Add iPay related fields and methods."""

    _inherit = "payment.transaction"

    ipay_txncd = fields.Char(
        "iPay Transaction ID", related="ipay_id.txncd", readonly=True
    )
    ipay_channel = fields.Char("iPay Channel", related="ipay_id.channel", readonly=True)
    ipay_id = fields.Many2one(
        "ipay.data",
        "iPay Transaction",
        readonly=True,
        help="Related payment details for the transaction",
    )
    ipay_amount = fields.Monetary(
        related="ipay_id.mc",
        currency_field="ipay_currency_id",
        string="Amount Paid",
        help="Amount paid by customer. \n\
                The currency may differ from that of the sales order itself",
    )
    ipay_currency_id = fields.Many2one(
        related="provider_id.ipay_currency_id", string="Currency(iPay)"
    )

    def _get_specific_rendering_values(self, processing_values):
        """Return a dict of provider-specific values used to render the redirect form.

        For an provider to add its own rendering values, it must overwrite this method and return a
        dict of provider-specific values based on the processing values (provider-specific
        processing values included).

        :param dict processing_values: The processing values of the transaction
        :return: The dict of provider-specific rendering values
        :rtype: dict
        """
        values = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != "ipayafrica":
            return values
        partner = self.env["res.partner"].browse(processing_values["partner_id"])
        processing_values.update(
            vendor=self.provider_id.ipay_vendor_id,
            currency_name=self.env["res.currency"]
            .browse(processing_values.get("currency_id"))
            .exists()
            .name,
            hash_key=self.provider_id.ipay_hash_key,
            callback_url=self.provider_id.ipay_callback_url,
            checkout_url=self.provider_id.ipay_checkout_url,
            live="1" if self.provider_id.state == "enabled" else "0",
            crl="0",  # request http[s] format for callback data
            partner_phone=partner.phone,
            partner_email=partner.email,
            amount=processing_values.get("amount") + self.fees,
        )
        # hash_key generation
        datastring = ""
        for key in FIELDS.split("."):
            datastring += str(processing_values[key])
        if datastring:
            processing_values.update(
                hash_key=hmac.HMAC(
                    bytes(self.provider_id.ipay_hash_key, "latin-1"),
                    bytes(datastring, "latin-1"),
                    hashlib.sha1,
                ).hexdigest()
            )
        return processing_values

    @api.model
    def _get_tx_from_notification_data(self, provider, data):
        """Find the transaction based on the pesapal notification data.

        For pesapal to handle transaction post-processing, it must overwrite this method and
        return the transaction matching the data.

        :param str provider: The provider of the provider that handled the transaction
        :param dict data: The notification data sent by pesapal
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        """
        reference = data.get("id")
        txn = self.search(
            [("reference", "=", reference), ("provider_code", "=", "ipayafrica")],
            limit=1,
        )
        if not txn:
            error_msg = (
                _(
                    "IPAY_AFRICA: Received data for Order reference %s, but no transaction found"
                )
                % reference
            )
            raise ValidationError(error_msg)
        return txn

    def _process_notification_data(self, data):
        """Validate payment and return dict of values to be used to update the payment transaction."""
        """Override of payment to process the transaction based on pesapal data.

        Note: self.ensure_one()

        :param dict data: The txn status notification data sent by pesapal
        :return: None
        :raise: ValidationError if inconsistent data were received
        """
        super()._process_notification_data(data)
        if self.provider_code != "ipayafrica":
            return
        pay = self.env["ipay.data"].sudo().save_data(data)
        status = data.get("status")
        self.ipay_id = pay
        self.provider_reference = pay.txncd
        status_message = "%s" % data
        if status in SUCCESS:
            if pay:
                pay.write(
                    {
                        "reconciled": True,
                        "provider_id": self.provider_id.id,
                        "currency_id": self.provider_id.ipay_currency_id.id,
                    }
                )
            self._set_done(state_message=status_message)
        elif status in PENDING:
            self._set_pending(state_message=status_message)
        elif status in FAILED:
            self._set_canceled(state_message=status_message)
        else:
            self._set_error(status_message)
