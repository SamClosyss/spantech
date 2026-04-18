/** @odoo-module **/

import { patch } from 'web.utils';
import { Record } from '@web/views/basic_relational_model';
import { KanbanRecordQuickCreate } from '@web/views/kanban/kanban_record_quick_create';
import BasicModel from "web.BasicModel";

patch(Record.prototype, 'user_recent_log/static/src/js/record_save.js', {
  async save(
        options = {
            stayInEdition: true,
            noReload: false,
            savePoint: false,
            useSaveErrorDialog: false,
        }
    ) {
  		var _super = await this._super(...arguments);
  		const changes = this.model.__bm__.__changes;
        var promise = Promise.resolve();
        if (!_.isEmpty(changes)){
            promise = this.model.__bm__._rpc({
                model: "user.recent.log",
                method: "get_recent_log",
                args: [this.resModel, this.data.id, changes],
            });
    	}
		return promise.then(() => {
		    return _super;
		});
	}
});

patch(KanbanRecordQuickCreate.prototype, 'user_recent_log/static/src/js/record_save.js', {
	setup() {
		this._super(...arguments);
		//create class object for call model method
		this.__kv__ = new BasicModel(this, {
            fields: this.props.record.fields || {},
            modelName: this.props.record.resModel,
            useSampleModel: false,
        });
	},
	_trigger_up(ev) {
        const evType = ev.name;
        const payload = ev.data;
        if (evType === "call_service") {
            let args = payload.args || [];
            if (payload.service === "ajax" && payload.method === "rpc") {
                // ajax service uses an extra 'target' argument for rpc
                args = args.concat(ev.target);
                return payload.callback(owl.Component.env.session.rpc(...args));
            } else if (payload.service === "notification") {
                return this.notificationService.add(payload.message, {
                    className: payload.className,
                    sticky: payload.sticky,
                    title: payload.title,
                    type: payload.type,
                });
            }
            throw new Error(`call service ${payload.service} not handled in relational model`);
        } 
    },
    async validate(mode) {
    	await this._super(this);
    	var isKanban = true
    	var changes = true
    	var id = this.props.record.resId.toString()
    	var resModel = this.props.record.resModel.toString()
    	if(id){
    		this.__kv__._rpc({
                model: "user.recent.log",
                method: "get_recent_log",
                args: [resModel, id, changes, isKanban],
            });
    	}
    }
});