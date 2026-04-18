odoo.define('website_sale_ext.attribute_accordian', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.AttributeFilterCollapse = publicWidget.Widget.extend({
        selector: '.wsale_accordion_collapsible',
        start: function () {
            this.$('.accordion-item').each(function () {
                const $item = $(this);
                const $checkboxes = $item.find('input[type="checkbox"]');
                const $select = $item.find('select');
                let hasSelectedValue = false;

                // Check if any checkbox is selected
                $checkboxes.each(function () {
                    if ($(this).is(':checked')) {
                        hasSelectedValue = true;
                        return false; // break
                    }
                });

                // Check if select has a selected value (other than empty)
                if (!hasSelectedValue && $select.length) {
                    $select.each(function () {
                        if ($(this).val()) {
                            hasSelectedValue = true;
                            return false; // break
                        }
                    });
                }

                if (!hasSelectedValue) {
                    const $collapse = $item.find('.accordion-collapse');
                    const $button = $item.find('.accordion-button');

                    // Collapse the accordion if no selected value
                    $collapse.removeClass('show');
                    $button.addClass('collapsed');
                }
            });
        }
    });
});
