/** @odoo-module **/
import { viewService } from "@web/views/view_service";

const originalStart = viewService.start;

viewService.start = function (env, deps) {
    const service = originalStart(env, deps);
    const orm = deps.orm;

    /**
     * Load Fields information
     * Used by model_field_hook.js
     */
    async function loadFields(resModel, options = {}) {
        return orm.call(resModel, "fields_get", [options.fieldNames, options.attributes]);
    }

    /**
     * Load Records
     * Inherited to load records in domain widget
     */
    async function loadRecords(resModel, options = {}) {
        const args = {
            domain: [],
            fields: ["id", "display_name"],
            context: { ...options.context, web_domain_widget: true },
        };
        return orm.call(resModel, "domain_search_read", [], args);
    }

    // Return the original service extended with our new methods
    return {
        ...service,
        loadFields,
        loadRecords,
    };
};
