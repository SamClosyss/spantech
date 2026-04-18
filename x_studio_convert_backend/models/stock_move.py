from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_tmpl_notes = fields.Text(related='product_id.product_tmpl_id.x_studio_product_notes',
                                     string='Product Notes')
    product_tmpl_hs_code = fields.Char(related='product_id.product_tmpl_id.x_studio_hs_code',
                                       string='Product HS Code')
    product_tmpl_country_of_origin = fields.Char(related='product_id.product_tmpl_id.x_studio_hs_code_1',
                                                 string='Product Country of Origin')


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_tmpl_notes = fields.Text(related='product_id.product_tmpl_id.x_studio_product_notes',
                                     string='Product Notes')

    # https://spantech.odoo.com/web#id=280&menu_id=554&cids=2%2C1%2C3&action=806&model=project.task&view_type=form
    @api.onchange('product_id', 'product_uom_id')
    def _onchange_product_id(self):
        res = super(StockMoveLine, self)._onchange_product_id()
        if self.product_id:
            self.description_picking = str(self.description_picking) + '\n' + str(self.product_tmpl_notes)
        return res

    # https://spantech.odoo.com/web#id=280&menu_id=554&cids=2%2C1%2C3&action=806&model=project.task&view_type=form
    def _get_aggregated_product_quantities(self, **kwargs):
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for aggregated_move_line in aggregated_move_lines:
            if aggregated_move_lines[aggregated_move_line]['product'] and aggregated_move_lines[aggregated_move_line][
                'product'].product_tmpl_id.x_studio_product_notes:
                aggregated_move_lines[aggregated_move_line]['description'] = str(
                    aggregated_move_lines[aggregated_move_line]['description']) + '\n' + aggregated_move_lines[
                                                                                 aggregated_move_line][
                                                                                 'product'].product_tmpl_id.x_studio_product_notes
        return aggregated_move_lines
