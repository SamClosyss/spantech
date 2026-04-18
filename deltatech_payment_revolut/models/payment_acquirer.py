# ©  2008-2021 Deltatech
# See README.rst file on addons root folder for license details


import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class PaymentAcquirer(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(selection_add=[("revolut", "Revolut")], ondelete={"revolut": "set default"})

    revolut_api_key = fields.Char()

    def _compute_feature_support_fields(self):
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == "revolut").update(
            {
                "support_manual_capture": True,
            }
        )

    @api.depends("code")
    def _compute_view_configuration_fields(self):
        res = super()._compute_view_configuration_fields()
        self.filtered(lambda acq: acq.code == "revolut").write(
            {
                "show_credentials_page": True,
                "show_allow_tokenization": True,
                "show_payment_icon_ids": True,
                "show_pre_msg": True,
                "show_pending_msg": True,
                "show_auth_msg": True,
                "show_done_msg": True,
                "show_cancel_msg": True,
            }
        )
        return res

    def _revolut_get_api_url(self):
        self.ensure_one()
        if self.state == "enabled":
            return "https://merchant.revolut.com/api/1.0"
        else:
            return "https://sandbox-merchant.revolut.com/api/1.0"

    def _get_default_payment_method_id(self, code):
        self.ensure_one()
        if self.code != "revolut":
            return super()._get_default_payment_method_id(code)
        return self.env.ref("deltatech_payment_revolut.payment_method_revolut").id
