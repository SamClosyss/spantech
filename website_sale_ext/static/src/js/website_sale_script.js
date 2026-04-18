/** @odoo-module **/

import "website_sale.website_sale";
import publicWidget from "web.public.widget";
import sAnimations from "website.content.snippets.animation";
import { qweb, _t } from "web.core";

publicWidget.registry.WebsiteSale.include({
    _onChangeCombination: function (ev, $parent, combination) {
        this._super.apply(this, arguments);
        if (combination.display_name) {
            const $extraFields =  $('.oe_website_sale').find('.o_wsdc_default_code_value');
            $extraFields.html(combination.display_name);
        }
    },
});

