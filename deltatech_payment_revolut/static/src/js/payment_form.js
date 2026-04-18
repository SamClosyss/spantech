odoo.define("deltatech_payment_revolut.payment_form", (require) => {
    "use strict";

    const checkoutForm = require("payment.checkout_form");
    const manageForm = require("payment.manage_form");
    const paymentTestMixin = {
        // --------------------------------------------------------------------------
        // Private
        // --------------------------------------------------------------------------

        _processDirectPayment: function (provider, acquirerId, processingValues) {
            if (provider !== "revolut") {
                return this._super(...arguments);
            }
            var self = this;
            RevolutCheckout(processingValues.public_id, processingValues.environment).then(function (instance) {
                // Work with instance:

                instance.payWithPopup({
                    name: processingValues.name,
                    email: processingValues.email,

                    onSuccess() {
                        return self
                            ._rpc({
                                route: "/payment/revolut/return",
                                params: {
                                    post: processingValues,
                                },
                            })
                            .then(() => {
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

        _prepareInlineForm: function (provider, paymentOptionId, flow) {
            if (provider !== "revolut") {
                return this._super(...arguments);
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
        },
    };
    checkoutForm.include(paymentTestMixin);
    manageForm.include(paymentTestMixin);
});
