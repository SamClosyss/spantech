
/** @odoo-module **/
import { patch } from 'web.utils';
import {EditMenuDialog} from '@website/components/dialog/edit_menu';
const { Component, useState, useEffect, onWillStart, useRef, onMounted } = owl;

patch(EditMenuDialog.prototype, 'website_preview_test_mode', {
       setup() {
        this._super.apply(this, arguments)
        onMounted(() => {
            this.$sortables = $(this.menuEditor.el);
            this.$sortables.nestedSortable({
                listType: 'ul',
                handle: 'div',
                items: 'li',
                maxLevels: 0,
                toleranceElement: '> div',
                forcePlaceholderSize: true,
                opacity: 0.6,
                placeholder: 'oe_menu_placeholder',
                tolerance: 'pointer',
                attribute: 'data-menu-id',
                expression: '()(.+)', // nestedSortable takes the second match of an expression (*sigh*)
                isAllowed: (placeholder, placeholderParent, currentItem) => {
                    return !placeholderParent
                        || !currentItem[0].dataset.isMegaMenu && !placeholderParent[0].dataset.isMegaMenu;
                },
            });
        });
    }
});
