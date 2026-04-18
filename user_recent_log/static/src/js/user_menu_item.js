/** @odoo-module **/

import { registry } from "@web/core/registry";

export function recentLogItem(env) {
    return {
        type: "item",
        id: "activity",
        description: env._t("Recent Logs"),
        callback: () => {
            env.services.action.doAction({
                type: "ir.actions.act_window",
                name: "User Recent Log(s)",
                res_model: "user.recent.log",
                views: [[false, "list"], [false, "form"], [false, "kanban"]],
            });
        },
        sequence: 45,
    };
}

registry.category("user_menuitems").add("recent_log", recentLogItem, { force: true })
