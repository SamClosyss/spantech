# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website.controllers.main import Website

class WebsiteHomePage(Website):
    @http.route('/', type='http', auth="public", website=True, sitemap=True)
    def index(self, **kw):
        res = super(WebsiteHomePage, self).index(**kw)
        prods = http.request.env['product.product'].sudo().search([('featured', '=', True)])
        res.qcontext.update({"featured_products": prods})
        return res

class SwaraShopKenya(http.Controller):  
   

    @http.route('/shipping/policy', auth='public', website=True)
    def shipping_policy(self, **kw):
        return http.request.render('swara_shop_kenya.shipping_policy')  

    @http.route('/refund/policy', auth='public', website=True)
    def refund_policy(self, **kw):
        return http.request.render('swara_shop_kenya.refund_policy')  

    @http.route('/term_of_service/policy', auth='public', website=True)
    def term_of_service_policy(self, **kw):
        return http.request.render('swara_shop_kenya.term_of_service')  

    @http.route('/privacy/policy', auth='public', website=True)
    def privacy_policy(self, **kw):
        return http.request.render('swara_shop_kenya.privacy_policy')  

