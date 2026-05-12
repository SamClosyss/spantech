from odoo import fields, models, api, _
from odoo.http import request

class ir_ui_menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def search(self, domain, offset=0, limit=None, order=None, **kwargs):
        count = kwargs.get('count', False)
        # In Odoo 17+, search() does not take 'count' argument.
        # We fetch all matching menus (offset=0, limit=None) and filter them manually.
        ids = super(ir_ui_menu, self).search(domain, offset=0, limit=None, order=order)
        user = self.env.user
        # user.clear_caches()
        cids = request and request.httprequest.cookies.get('cids') and request.httprequest.cookies.get('cids').split(',')[0] or self.env.company.id
        for menu_id in user.access_management_ids.filtered(lambda line: int(cids) in line.company_ids.ids).mapped('hide_menu_ids'):
            if menu_id in ids:
                ids = ids - menu_id
        if offset:
            ids = ids[offset:]
        if limit:
            ids = ids[:limit]
        return len(ids) if count else ids

