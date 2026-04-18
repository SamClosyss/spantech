# -*- coding: utf-8 -*-
# Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.osv.expression import AND
from datetime import datetime
from odoo.addons.website_sale.controllers.main import TableCompute

class BizopleWebsiteSale(WebsiteSale):

    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        show_instock = post.get('show_instock', False)
        res = super().shop(page, category, search, min_price, max_price, ppg, **post)
        keepQueryargs = res.qcontext.get('keep', {}).args
        keepQueryargs.update({'show_instock': show_instock})
        res.qcontext.update({'show_instock': show_instock})

        attrib_set = res.qcontext.get('attrib_set', set())
        website = request.env['website'].get_current_website()
        ppr = website.shop_ppr or 4
        ppg = int(ppg) if ppg else website.shop_ppg or 20

        if show_instock and attrib_set:
            dom = [
                ('qty_available', '>', 0),
                ('is_published', '=', True),
                ('website_id', '=', website.id),
                ('sale_ok', '=', True)
            ]
            if category:
                dom.append(('public_categ_ids.id', 'in', [category.id]))

            variants = request.env['product.product'].sudo().search(dom)

            attrib_vals = request.env['product.attribute.value'].browse(list(attrib_set))
            attrib_map = {}
            for val in attrib_vals:
                attrib_map.setdefault(val.attribute_id.id, set()).add(val.id)

            filtered_variants = variants.filtered(
                lambda v: all(
                    any(val.product_attribute_value_id.id in val_ids for val in v.product_template_attribute_value_ids)
                    for val_ids in attrib_map.values()
                )
            )

            template_ids = list(set(filtered_variants.mapped('product_tmpl_id').ids))
            products = request.env['product.template'].sudo().search([('id', 'in', template_ids)])
            
            attrib_list = request.httprequest.args.getlist('attrib')
            attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
            attributes_ids = {v[0] for v in attrib_values}
            attrib_set = {v[1] for v in attrib_values}
            if attrib_list:
                post['attrib'] = attrib_list
            
            pager = request.website.pager(
                url="/shop",
                total=len(products),
                page=page,
                step=ppg,
                scope=7,
                url_args=post
            )
            offset = pager['offset']
            page_products = products[offset: offset + ppg]

            now = datetime.timestamp(datetime.now())
            pricelist = request.env['product.pricelist'].browse(request.session.get('website_sale_current_pl'))
            if not pricelist or request.session.get('website_sale_pricelist_time', 0) < now - 3600:
                pricelist = website.get_current_pricelist()
                request.session['website_sale_pricelist_time'] = now
                request.session['website_sale_current_pl'] = pricelist.id

            product_prices = page_products._get_sales_prices(pricelist)
            bins = TableCompute().process(page_products, ppg, ppr)

            res.qcontext.update({
                'products': page_products,
                'bins': bins,
                'products_prices': product_prices,
                'get_product_prices': lambda product: product_prices.get(product.id),
                'pager': pager,
            })
        return res
