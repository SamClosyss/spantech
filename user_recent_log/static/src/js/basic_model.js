odoo.define("user_recent_log.CustomBasicModel", function (require) {

    var BasicModel = require("web.BasicModel");

    BasicModel.include({
        init: function (parent, params) {
            this.__changes = null;
            this._super.apply(this, arguments);
        },

        _generateChanges: function (record, options) {
            const _super = this._super.bind(this);
            const res = _super(record, options);
            if (record.model != 'res.config.settings'){
                this.__changes = res
            }
            return res
        },
    });
});
