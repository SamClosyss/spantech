/** @odoo-module **/

import Dialog from 'web.Dialog';
import core from 'web.core';
import options from 'web_editor.snippets.options';
import { loadBundle } from "@web/core/assets";

const _t = core._t;

options.registry.EmbedVideo = options.Class.extend({
    //--------------------------------------------------------------------------
    // Options
    //--------------------------------------------------------------------------

    async editVideo() {
        const $container = this.$target.find('.embed_video_embedded');
        const $video_src = this.$target.find('source');
        const $video_url = this.$target.find('source').attr('src');
        const video = $container.html().trim();
        debugger

        await loadBundle({
            jsLibs: [
                '/web/static/lib/ace/ace.js',
                '/web/static/lib/ace/mode-xml.js',
                '/web/static/lib/ace/mode-qweb.js',
            ],
        });

        await new Promise(resolve => {
            const $content = $(core.qweb.render('website_sale_ext.custom_video_dialog_content'));
            $content.find('#video_url').val($video_url)
            const dialog = new Dialog(this, {
                title: _t("Edit embedded video"),
                $content,
                buttons: [
                    {
                        text: _t("Save"),
                        classes: 'btn-primary',
                        click: async () => {
                            $video_src.attr('src',$('#video_url').val());
                            $video_src.parent().removeClass('d-none');
                            $container.addClass('d-none');
                        },
                        close: true,
                    },
                    {
                        text: _t("Discard"),
                        click: async () => {
                            $container.removeClass('d-none');
                            $video_src.parent().removeClass('d-none').addClass('d-none');
                        },
                        close: true,
                    },
                ],
            });
            dialog.on('closed', this, resolve);
            dialog.open();
        });
    },
});

export default {
    EmbedVideo: options.registry.EmbedVideo,
};
