from odoo import api, models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    ag_delivery_no = fields.Char(string="AG Delivery Number", compute="get_number")
    packages_number = fields.Integer(string="packages Number")

    def get_number(self):
        """
        Use: Get Numeric value from picking name
        Added by: Jignesh
        Added on: 1/10/22
        Task: https://spantech.odoo.com/web#id=654&menu_id=554&cids=1%2C2%2C3%2C4&action=806&model=project.task&view_type=form
        """
        for picking in self:
            if picking.name:
                ag_delivery_no = ''.join([n for n in picking.name if n.isdigit()])
                if not ag_delivery_no:
                    picking.ag_delivery_no = picking.name
                else:
                    picking.ag_delivery_no = ag_delivery_no
            else:
                picking.ag_delivery_no = ''

    def do_print_shipping_invoice(self):
        """
        Use: Print Shipping Invoice
        Added by: Jignesh
        Added on: 16/11/22
        Task: https://spantech.odoo.com/web?debug=1#id=721&cids=7%2C4%2C3%2C2%2C1&menu_id=554&action=806&model=project.task&view_type=form
        """
        for picking in self:
            for invoice in picking.invoice_ids:
                invoice.picking_schedule_date = picking.scheduled_date

                invoice.picking_date_done = picking.date_done
                invoice.picking_user_id = picking.user_id.id
                invoice.picking_packages_number  = picking.packages_number
                invoice.picking_delivery_note = picking.note
                return self.env.ref('pdf_report.ag_shipping_invoice').report_action(invoice)
        return True
