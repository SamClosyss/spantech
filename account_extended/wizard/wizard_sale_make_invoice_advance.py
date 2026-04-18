from odoo import models, fields, api, _


class WizardSaleMakeInvoiceAdvance(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):
        """
        Use: Inherited method to parse customer reference.
        :return: super method response
        """
        # TODO: please test this using debug maybe the v16 method is different
        ctx = self._context.copy()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        so_ids = sale_orders.filtered(lambda so: so.client_order_ref)
        if so_ids:
            ctx.update({'default_ref': ', '.join(so_ids.mapped('client_order_ref'))})
        return super(WizardSaleMakeInvoiceAdvance, self.with_context(ctx)).create_invoices()
