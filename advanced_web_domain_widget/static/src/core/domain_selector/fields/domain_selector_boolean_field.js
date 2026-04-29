/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

import { Component } from "@odoo/owl";

const dsf = registry.category("domain_selector/fields_bits");

export class DomainSelectorBooleanFieldBits extends Component {
    onChange(ev) {
        this.props.update({
            value: ev.target.value === "1",
        });
    }
}
Object.assign(DomainSelectorBooleanFieldBits, {
    template: "advanced_web_domain_widget.DomainSelectorBooleanFieldBits",

    onDidTypeChange() {
        return { value: true };
    },
    getOperators() {
        return [
            {
                category: "equality",
                label: _t("is"),
                value: "=",
                onDidChange() {},
                matches({ operator }) {
                    return operator === this.value;
                },
            },
            {
                category: "equality",
                label: _t("is not"),
                value: "!=",
                onDidChange() {},
                matches({ operator }) {
                    return operator === this.value;
                },
            },
        ];
    },
});

dsf.add("boolean", DomainSelectorBooleanFieldBits);
