odoo.define('swara_web.script', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var core = require('web.core');
var _t = core._t;

var timeout;

    publicWidget.registry.websiteSwaraScript = publicWidget.Widget.extend({
        selector: '#wrapwrap',
        events: {
            'click .swara_header .swara_searchbar_action': '_onSearchClickOpen',
            'click .swara_header .swara_searchbar_close': '_onSearchClickClose',
        },

        _onSearchClickOpen: function (ev) {
            $(".te_search_icon_4").css("display", "inline-block");
            $(".swara_search_container").css("height",$('header#top').height()+ 'px')
            $(".swara_search_container").addClass("visible");
            setTimeout(function(){
                $('.o_wsale_products_searchbar_form input[name="search"]').focus();
            }, 500);
        },

        _onSearchClickClose: function(ev) {
            $(".swara_search_container").removeClass("visible");
            $('.swara_form input[name=search]').val('')
        },

    });

});