# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    is_mass_production = fields.Boolean(string='Is Lot No Generated', copy=False)
    tracking = fields.Selection(
        'Product Tracking', related='product_id.tracking', help='Technical: used in views only.')
    lot_ids = fields.Many2many('stock.lot', 'rel_production_stock_production', 'production_id', 'lot_id',
                               copy=False)

    def mass_produce(self):
        self.ensure_one()
        view = self.env.ref('bi_mrp_assign_serial_number.view_mrp_production_assign_serial_number')
        ctx = self._context.copy()
        ctx.update({'default_product_id': self.product_id.id,
                    'default_product_qty': self.product_qty,
                    'default_production_id': self.id,
                    })
        return {
            'name': 'Assigning Mass Serial No',
            'view_mode': 'form',
            'res_model': 'mrp.production.assign',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'context': ctx,
            'target': 'new',
        }

    def _post_inventory(self, cancel_backorder=False):
        for order in self:
            moves_not_to_do = order.move_raw_ids.filtered(lambda x: x.state == 'done')
            moves_to_do = order.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
            for move in moves_to_do.filtered(lambda m: m.product_qty == 0.0 and m.quantity_done > 0):
                move.product_uom_qty = move.quantity_done
            # MRP do not merge move, catch the result of _action_done in order
            # to get extra moves.
            moves_to_do = moves_to_do._action_done()
            moves_to_do = order.move_raw_ids.filtered(lambda x: x.state == 'done') - moves_not_to_do
            if self.is_mass_production:
                qty = self.product_qty / len(self.lot_ids)
                for lot_id in self.lot_ids:
                    finish_moves = order.move_finished_ids.filtered(
                        lambda m: m.product_id == order.product_id and m.lot_id == lot_id and m.state not in (
                        'done', 'cancel'))
                    # the finish move can already be completed by the workorder.
                    if not finish_moves.quantity_done:
                        finish_moves.quantity_done = qty
                        finish_moves.move_line_ids.lot_id = lot_id
            else:
                finish_moves = order.move_finished_ids.filtered(
                    lambda m: m.product_id == order.product_id and m.state not in ('done', 'cancel'))
                # the finish move can already be completed by the workorder.
                if not finish_moves.quantity_done:
                    finish_moves.quantity_done = float_round(order.qty_producing - order.qty_produced,
                                                             precision_rounding=order.product_uom_id.rounding,
                                                             rounding_method='HALF-UP')
                    finish_moves.move_line_ids.lot_id = order.lot_producing_id
            order._cal_price(moves_to_do)

            moves_to_finish = order.move_finished_ids.filtered(lambda x: x.state not in ('done', 'cancel'))
            moves_to_finish = moves_to_finish._action_done(cancel_backorder=cancel_backorder)
            order.action_assign()
            consume_move_lines = moves_to_do.mapped('move_line_ids')
            order.move_finished_ids.move_line_ids.consume_line_ids = [(6, 0, consume_move_lines.ids)]
        return True

class InheritedStockMove(models.Model):
    _inherit = 'stock.move'

    lot_id = fields.Many2one('stock.lot', string="Lot No")
