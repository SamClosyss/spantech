odoo.define('website_sale_ext.menu', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var animations = require('website.content.snippets.animation');

require('web.dom_ready');


$('[hb_href]').click(function(ev){
    window.location.href = $(ev.currentTarget).attr('hb_href');

})

publicWidget.registry.hoverableDropdown.include({

    _dropdownHover: function () {
        return;
    },

});

});


