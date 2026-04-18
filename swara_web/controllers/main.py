# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Controller, route
from odoo.addons.http_routing.models.ir_http import slug
from werkzeug.exceptions import NotFound
from odoo.addons.website.controllers.main import QueryURL


class TableCompute(object):

    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey, ppr):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= ppr:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(ppr):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products, ppg=20, ppr=4):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in products:
            x = min(max(p.website_size_x, 1), ppr)
            y = min(max(p.website_size_y, 1), ppr)
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % ppr, pos // ppr, x, y, ppr):
                pos += 1
            # if 21st products (index 20) and the last line is full (ppr products in it), break
            # (pos + 1.0) / ppr is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                break

            if x == 1 and y == 1:  # simple heuristic for CPU optimization
                minpos = pos // ppr

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
            self.table[pos // ppr][pos % ppr] = {
                'product': p, 'x': x, 'y': y,
                'ribbon': p._get_website_ribbon(),
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // ppr))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]

        return rows


class SwaraCollections(http.Controller):

    @http.route(['/collection/<model("swara.collections"):collection>',
                 '/collection/<model("swara.collections"):collection>/page/<int:page>',
                 '/collection/<model("swara.collections"):collection>/category/<model("product.public.category"):category>',
                 '/collection/<model("swara.collections"):collection>/category/<model("product.public.category"):category>/page/<int:page>',],
                type='http', auth="public", website=True, sitemap=True)
    def swara_collection(self, page=0, collection=None, category='', **post):

        url = "/collection/%s" % collection.id
        Products_in_collection = collection.sudo().product_ids
        Products = collection.sudo().product_ids
        Category = request.env['product.public.category']
        keep = QueryURL(url, category=category and int(category), order=post.get('order'))
        if category:
            category = Category.search([('id', '=', int(category))], limit=1)
            Products = Products.filtered(lambda prod: category.id in prod.public_categ_ids.ids )
            if not category or not category.can_access_from_current_website():
                raise NotFound()
        else:
            category = ''
        if Products:
            Products = request.env['product.template'].search([('id', 'in', Products.ids)], order=post.get('order'))
        categories = Products_in_collection.mapped('public_categ_ids')

        if category:
            url += "/category/%s" % slug(category)
        pager = request.website.pager(url=url, total=len(Products), page=page, step=8, scope=7, url_args=post)
        offset = pager['offset']
        product_count = len(Products)
        Products = Products[offset:offset + 8]

        values = {
            'collection': collection,
            'category': category,
            'categories': categories,
            'products': Products,
            'product_count':product_count,
            'bins': TableCompute().process(Products, 8, 4),
            'pager': pager,
            'keep': keep,
            'image_url': '/web/image/swara.collections/%s/image/' % collection.id
        }
        return request.render("swara_web.collection_template", values)

    @http.route(['/collection/product/<model("product.template"):product>'],
                type='http', auth="public", website=True, sitemap=True)
    def swara_product_collection(self, product=False, **post):
        values = {
                'product':product,
        }
        return request.render("swara_web.collection_product_template", values)