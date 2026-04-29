from builtins import super

from odoo import api, fields, models, _
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from _datetime import datetime


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # def get_purchase_orders(self):
    #     self.ensure_one()
    #     purchase_order_ids = (
    #                 self.procurement_group_id.stock_move_ids.created_purchase_line_id.order_id | self.procurement_group_id.stock_move_ids.move_orig_ids.purchase_line_id.order_id).ids
    #     po = self.env['purchase.order'].browse(purchase_order_ids)
    #     return po
    #
    # @api.depends('procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.partner_requirement')
    # def _get_requirements(self):
    #     """
    #     Use: Get Special requirements from related SO
    #     Added by: Jignesh
    #     Added on: 17/3/23
    #     Task: https://spantech.odoo.com/web#id=857&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    #     """
    #     for production in self:
    #         production.requirement = production.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.partner_requirement
    #         production.sale_id = production.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id.id
    #
    # # https://spantech.odoo.com/web#id=857&menu_id=554&cids=7%2C4%2C3%2C2%2C1&action=806&model=project.task&view_type=form
    # requirement = fields.Text("Customer Special Requirements", compute='_get_requirements', store=True, readonly=False,
    #                           groups="sales_team.group_sale_manager")
    # sale_id = fields.Many2one("sale.order", compute=_get_requirements, store=True)
    # certified_by = fields.Many2one("res.users", string="Certified By")

    # https://spantech.odoo.com/web?debug=1#id=1002&menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5%2C10%2C9&action=806&model=project.task&view_type=form
    components_ids = fields.One2many("mrp.components", "mo_id", string="Components")
    cylinder_ids = fields.One2many("mrp.cylinder", "mo_id", string="Components")

    valid_date = fields.Datetime(string='Valid Date', compute='_compute_valid_date')
    logo_use = fields.Selection([
            ('AGGlabel', 'AGG Label'), 
            ('cac_label', 'CAC Label'), 
            ('all_in_gas', 'All In Gas'),
            ('kimessa_label', 'Kimessa Label'),
            ('gas_tech', 'Gas Tech'),
            ('gas_alarm', 'Gas Alarm'),
            ('encore_monitoring', 'Encore Monitoring'),
            ('CAC_gas_asia', 'CAC Gas Asia'),
            ('CAC_gas_instrumentation', 'CAC Gas Instrumentation'),
            ('NZ_safety_blackwoods', 'NZ Safety Blackwoods'),
            ('mine_safety', 'Mine Safety'),
            ('skill_pro', 'Skillpro'),
            ('alliance_safety', 'Alliance Safety'),
            ('custom', 'Custom')], 
            default='AGGlabel', string="Logo Use")
    logo = fields.Binary(string="Custom Logo")
    all_in_gas_label_custom_logo = fields.Binary(help="Recommended size: 1477 x 171 only.", string="Custom Logo")

    is_ag_backorder_of_cylinders = fields.Boolean()
    mark_done_date = fields.Datetime(string='Mark As Done Date')

    @api.constrains('cylinder_ids')
    def _check_cylinder_ids(self):
        for rec in self:
            if rec.cylinder_ids and len(rec.cylinder_ids) != rec.product_qty:
                raise UserError(
                    _("You cannot create cylinder serial number more then or less then manufacturer produce qty"))

    @api.depends('product_id', 'date_start')
    def _compute_valid_date(self):
        months = self.product_id.product_tmpl_id.useable_time_span or 0
        #self.valid_date = self.date_planned_start + timedelta(days=days)
        self.valid_date = self.date_start + relativedelta(months=months)

    def print_bottle_label_pdf(self):
        cylinders = self.env['mrp.cylinder'].search(
            [('mo_id', '=', self.id)])
        for rec in cylinders:
            rec.generate_qr()
        return self.env.ref('pdf_report.action_bottle_label_report_pdf').report_action(self)

    def print_certificate_pdf(self):
        return self.env.ref('pdf_report.action_certificate_report_pdf').report_action(self)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        components_ids_data = [fields.Command.clear()]
        components_ids_data += [fields.Command.create(line._prepare_order_line_values()) for line in
                                self.product_id.components_ids]
        self.components_ids = components_ids_data

    @api.model
    def create(self, vals):
        res = super(MrpProduction, self).create(vals)
        for rec in res:
            rec._onchange_product_id()
        return res

    def button_mark_done(self):
        if not self._context.get('BACKORDER', False):
            for order in self.filtered(lambda o: o.company_id.id == 7 and o.state != 'done'):
                serial_number = ""
                if not order.cylinder_ids or len(order.cylinder_ids) != order.product_qty:
                    raise UserError(
                        _(
                            "Please set proper cylinder serial number. "
                            "Cylinder serial number must match the manufacturing quantity."
                        )
                    )

                # Create record of stock.assign.serial
                for cylinder in order.cylinder_ids:
                    serial_number += "%s\n" % cylinder.name

                next_serial = self.env['stock.lot']._get_next_serial(order.company_id, order.product_id)
                stock_assign_serial = self.env['stock.assign.serial'].create({
                    'production_id': order.id,
                    'expected_qty': order.product_qty,
                    'serial_numbers': serial_number,
                    'next_serial_number': 1,
                    'next_serial_count': order.product_qty - order.qty_produced,
                })
                stock_assign_serial.apply()
                order.is_ag_backorder_of_cylinders = True

                # Move serial/lot number validation INSIDE the loop
                for move in order.move_raw_ids:
                    for line in move.move_line_ids:
                        if line.product_id.tracking != 'none' and not line.lot_id:
                            raise UserError(_(
                                "Missing serial/lot number for product '%s' in raw material move.\n"
                                "Please ensure all tracked products have assigned lot or serial numbers before marking the order as done."
                            ) % line.product_id.display_name)

            # Now write for all valid records
            self.write({'mark_done_date': fields.Date.today()})

        return super(MrpProduction, self).button_mark_done()


    def button_mark_done_all_backorders(self):
        """
        Use: Mark As Done all the Backorders which is created from cylinders process
        Added by: Jignesh
        Added on: 3/6/23
        Task:
        """
        for backorder in self.procurement_group_id.mrp_production_ids.filtered(lambda b: b.company_id.id == 7):
            if backorder.state != 'done':
                backorder.with_context(BACKORDER=True).button_mark_done()
            else:
                backorder.is_ag_backorder_of_cylinders = False
    
    @api.depends('product_id', 'mark_done_date')
    def get_valid_until_date(self):
        shelf_month = self.product_id.x_studio_shelf_life_months
        if self.mark_done_date and shelf_month > 0:
            valid_until_date = (self.mark_done_date + relativedelta(months=shelf_month)).strftime('%d-%m-%Y')
            return valid_until_date
            
    @api.depends('product_id', 'mark_done_date')
    def get_valid_until_date_dateformat(self):
        shelf_month = self.product_id.x_studio_shelf_life_months
        if self.mark_done_date and shelf_month > 0:
            valid_until_date = (self.mark_done_date + relativedelta(months=shelf_month)).strftime('%d/%m/%Y')
            return valid_until_date

    def print_cac_label_pdf(self):
        return self.env.ref('pdf_report.action_cac_label_report_pdf').report_action(self)

    def print_qr_code(self):
        cylinders = self.env['mrp.cylinder'].search(
            [('mo_id', '=', self.id)])
        for rec in cylinders:
            rec.generate_qr()
        return self.env.ref('pdf_report.action_print_qr_code_report').report_action(self)

    def print_cac_nrc_certificate(self):
        return self.env.ref('pdf_report.action_cac_nrc_certificate_report').report_action(self)

    def print_cac_hpc_certificate(self):
        return self.env.ref('pdf_report.action_cac_hpc_certificate_report').report_action(self)

    def print_all_in_gas(self):
        return self.env.ref('pdf_report.action_all_in_gas_label_report').report_action(self)
        
    def print_cac_box_label(self):
        return self.env.ref('pdf_report.action_cac_box_label_report').report_action(self)
        
    def print_kimessa_pdf(self):
        cylinders = self.env['mrp.cylinder'].search(
            [('mo_id', '=', self.id)])
        for rec in cylinders:
            rec.generate_qr()
        return self.env.ref('pdf_report.action_kimessa_report').report_action(self)
        
    def print_all_in_gas_certificate_pdf(self):
        return self.env.ref('pdf_report.action_all_in_gas_certificate_report_pdf').report_action(self)
        
    def print_cac_nkd_label(self):
        return self.env.ref('pdf_report.action_cac_nkd_report').report_action(self)
    
    def print_all_in_gas_krapp(self):
        return self.env.ref('pdf_report.action_all_in_gas_krapp_label_report').report_action(self)
    
    # new 9 reports  
    def print_gas_tech(self):
        return self.env.ref('pdf_report.action_gas_tech_report').report_action(self)
        
    def print_gas_alarm(self):
        return self.env.ref('pdf_report.action_gas_alarm_report').report_action(self)
        
    def print_encore_monitoring(self):
        return self.env.ref('pdf_report.action_encore_monitoring_report').report_action(self)
        
    def print_CAC_gas_asia(self):
        return self.env.ref('pdf_report.action_CAC_gas_asia_report').report_action(self)
        
    def print_CAC_gas_instrumentation(self):
        return self.env.ref('pdf_report.action_CAC_gas_instrumentation_report').report_action(self)
        
    def print_NZ_safety_blackwoods(self):
        return self.env.ref('pdf_report.action_NZ_safety_blackwoods_report').report_action(self)
        
    def print_mine_safety(self):
        return self.env.ref('pdf_report.action_mine_safety_report').report_action(self)
        
    def print_skillpro(self):
        return self.env.ref('pdf_report.action_skillpro_report').report_action(self)
        
    def print_alliance_safety(self):
        return self.env.ref('pdf_report.action_alliance_safety_report').report_action(self)
        
    

