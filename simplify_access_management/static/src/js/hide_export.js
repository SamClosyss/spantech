/* @odoo-module */

import { ListController } from "@web/views/list/list_controller";
import { session } from "@web/session";
import { patch } from "@web/core/utils/patch";
import { onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        onWillStart(async () => {
            await this.is_hide_export();
        });
    },
    async is_hide_export(){
        let model = this.props.resModel;
        let cids = this.userService.context.allowed_company_ids
        let sam_hide_export = await rpc.query({
            model: "access.management",
            method: "is_export_hide",
            args: [session.user_id, cids, model],
        });  
        if (sam_hide_export){
            this.isExportEnable = false;
        }else{
            this.isExportEnable = await this.userService.hasGroup("base.group_allow_export");
        }
    }
})