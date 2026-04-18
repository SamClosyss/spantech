# -*- coding: utf-8 -*-
# Copyright (c) 2022-Present Mentis Consultancy Services. (<https://mcss.odoo.com>)

from odoo import api, fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('pesapal', 'Pesapal')], ondelete={'pesapal': 'set default'})
    pesapal_consumer_key = fields.Char('Consumer Key', required_if_provider='pesapal')
    pesapal_consumer_secret = fields.Char('Consumer Secret', required_if_provider='pesapal')

    @api.model
    def _get_compatible_providers(self, *args, currency_id=None, **kwargs):
        """ Override of payment to unlist Pespala providers for unsupported currencies. """
        providers = super()._get_compatible_providers(*args, currency_id=currency_id, **kwargs)

        currency = self.env['res.currency'].browse(currency_id).exists()
        if currency and currency.name not in ['USD', 'KES', 'UGX', 'TZS', 'MWK', 'RWF', 'ZMW', 'ZWL']:
            providers = providers.filtered(
                lambda a: a.code != 'pesapal'
            )

        return providers

    def _get_pesapal_urls(self):
        """ Pesapal URLS """
        if self.state == 'enabled':
            return 'https://pay.pesapal.com/v3'
        return 'https://cybqa.pesapal.com/pesapalv3'
