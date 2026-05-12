/** @odoo-module */

import { PaymentForm } from '@payment/interactions/payment_form';
import { patch } from '@web/core/utils/patch';
import { rpc } from '@web/core/network/rpc';

patch(PaymentForm.prototype, {

    async _processDirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode !== "revolut") {
            return super._processDirectFlow(...arguments);
        }

        RevolutCheckout(processingValues.public_id, processingValues.environment).then((instance) => {
            // Work with instance:
            instance.payWithPopup({
                name: processingValues.name,
                email: processingValues.email,

                onSuccess() {
                    return rpc("/payment/revolut/return", {
                        post: processingValues,
                    }).then(() => {
                        window.location = "/payment/status";
                    });
                },
                onError() {
                    window.location = "/shop/payment";
                },
                onCancel() {
                    location.reload();
                },
            });
        });
    },

    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== "revolut") {
            return super._prepareInlineForm(...arguments);
        } else if (flow === "token") {
            return Promise.resolve();
        }
        this._setPaymentFlow("direct");

        /* eslint no-unused-expressions: "off"*/
        !(function (e, o, t) {
            e[t] = function (public_id, environment) {
                var c = {
                    sandbox: "https://sandbox-merchant.revolut.com/embed.js",
                    prod: "https://merchant.revolut.com/embed.js",
                    dev: "https://merchant.revolut.codes/embed.js",
                };
                var d = o.createElement("script");
                d.id = "revolut-checkout";
                d.src = c[environment] || c.prod;
                d.async = !0;
                o.head.appendChild(d);
                var s = {
                    then: function (onFulfilled, onRejected) {
                        d.onload = function () {
                            onFulfilled(e[t](public_id));
                        };
                        d.onerror = function () {
                            o.head.removeChild(d);
                            if (onRejected) {
                                onRejected(new Error(t + " is failed to load"));
                            }
                        };
                    },
                };
                return typeof Promise === "function" ? Promise.resolve(s) : s;
            };
        })(window, document, "RevolutCheckout");

        return Promise.resolve();
    }
});
