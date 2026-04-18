# -*- coding: utf-8 -*-
import xlsxwriter
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError
import base64
import xlrd


class MrpProductionAssign(models.TransientModel):
    _name = 'mrp.production.assign'
    _description = 'Assign MRP orders'

    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_qty = fields.Integer('Quantity')
    assign_serial_number = fields.Char('Scan Lot')
    next_qty = fields.Integer(string='Next Quantity')
    to_serial_number = fields.Integer(string='To Serial Number')
    lot_line_ids = fields.One2many( 'lot.list', 'mrp_assign_id', string="Lot List")
    import_file = fields.Binary(string='File To Import')
    file_name = fields.Char("File Name")
    production_id = fields.Many2one('mrp.production', string='Production')
    to_serial_number_generator = fields.Selection([('manually', 'Enter Serial Number Manually'), ('import_file', 'File To Import')], default='manually')

    def import_xls_file(self):
        if self.import_file:
            data = base64.decodebytes(self.import_file)
            workbook = xlrd.open_workbook(file_contents=data)
            worksheet = workbook.sheet_by_index(0)
            if worksheet.nrows > self.product_qty:
                raise UserError('Please Enter the Lot/serial Number in Excel file.')
            for column in range(worksheet.ncols):
                for row in range(worksheet.nrows):
                    lot_number = worksheet.cell_value(row, column)
                    line_vals = {
                        'name': lot_number,
                        'mrp_assign_id': self.id,
                    }
                    lot_line_list = self.env['lot.list'].create(line_vals)
        else:
            raise UserError('Please select the file.') 
        return {
            'name': 'Assigning Mass Serial Numbers',
            'view_mode': 'form',
            'res_model': 'mrp.production.assign',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def click_generate(self):
        if self.to_serial_number != 0:
            if self.next_qty == 0:
                raise UserError('Please Enter the Next Quantity .')
            if self.next_qty - self.to_serial_number + 1 > self.product_qty:
                raise UserError('Please Enter the valid Quantity')
            lot_number = ''
            lot_string = ''

            for lot_id in self.assign_serial_number:
                if lot_id.isdigit():
                    lot_number += lot_id
                else:
                    lot_string += lot_id
    
            lot = self.assign_serial_number
            for i in range(self.to_serial_number, self.next_qty + 1):
                next_lot = lot_string + ('0' * 9)[-3:]
                next_lot = next_lot + str(i)
                line_vals = {
                    'name': next_lot,
                    'mrp_assign_id': self.id,                    }

                lot_line_list = self.env['lot.list'].create(line_vals)
        else:
            raise UserError('"To Serial Number" is grater than "0".')             

        return {
            'name': 'Assigning Mass Serial Numbers',
            'view_mode': 'form',
            'res_model': 'mrp.production.assign',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def create_serial_number(self):
        move_vals = []
        if len(self.lot_line_ids) <= 0:
            raise UserError('Please Generate number.')
        for rec in self.lot_line_ids:
            production_lot = self.env['stock.lot'].search(
                [('product_id', '=', self.product_id.id), ('name', '=', rec.name)])
            if production_lot:
                raise UserError('Serial number already exist for this product.')
            else:
                vals = {
                    'name': rec.name,
                    'product_id': self.product_id.id,
                    'company_id': self.env.user.company_id.id,
                }
                lot_id = self.env['stock.lot'].create(vals)
                self.production_id.lot_ids = [(4, lot_id.id)]
                self.production_id.is_mass_production = True
                qty = self.product_qty / len(self.lot_line_ids)
                group_orders = self.production_id.procurement_group_id.mrp_production_ids
                move_dest_ids = self.production_id.move_dest_ids
                byproduct_id = False
                print("First Method")
                if len(group_orders) > 1:
                    move_dest_ids |= group_orders[0].move_finished_ids.filtered(
                        lambda m: m.product_id == self.production_id.product_id).move_dest_ids
                date_planned_finished = self.production_id.date_planned_start + relativedelta(
                    days=self.production_id.product_id.produce_delay)
                date_planned_finished = date_planned_finished + relativedelta(
                    days=self.production_id.company_id.manufacturing_lead)
                if date_planned_finished == self.production_id.date_planned_start:
                    date_planned_finished = date_planned_finished + relativedelta(hours=1)
                move_vals.append({
                    'product_id': self.product_id.id,
                    'product_uom_qty': qty,
                    'product_uom': self.product_id.uom_id.id,
                    'operation_id': False,
                    'byproduct_id': byproduct_id,
                    'name': self.production_id.name,
                    'date': date_planned_finished,
                    'date_deadline': self.production_id.date_deadline,
                    'picking_type_id': self.production_id.picking_type_id.id,
                    'location_id': self.production_id.product_id.with_company(
                        self.production_id.company_id).property_stock_production.id,
                    'location_dest_id': self.production_id.location_dest_id.id,
                    'company_id': self.production_id.company_id.id,
                    'production_id': self.production_id.id,
                    'lot_id': lot_id.id,
                    'warehouse_id': self.production_id.location_dest_id.warehouse_id.id,
                    'origin': self.production_id.name,
                    'group_id': self.production_id.procurement_group_id.id,
                    'propagate_cancel': self.production_id.propagate_cancel,
                    'move_dest_ids': [(4, x.id) for x in self.production_id.move_dest_ids if not byproduct_id],
                })
                old_move = self.env['stock.move'].search(
                    [('production_id', '=', self.production_id.id), ('product_id', '=', self.product_id.id)])
                old_move.unlink()
                move_id = self.env['stock.move'].create(move_vals)
                for move in move_id:
                    print(move.name, 'Move')


class LotList(models.TransientModel):
    _name = "lot.list"
    _description = 'Lot list'

    name = fields.Char(string='Lot Number')
    mrp_assign_id = fields.Many2one('mrp.production.assign')
