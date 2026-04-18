from odoo import api, fields, models
from odoo.tools import float_compare, float_is_zero


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    x_is_corrected_line = fields.Boolean(default=False)

    # only for user input/visualization
    x_quantity = fields.Float(compute='_x_compute_reverse', digits='Product Unit of Measure', readonly=False)
    x_price_subtotal = fields.Float(compute='_x_compute_reverse', store=False, readonly=True)
    x_price_total = fields.Float(compute='_x_compute_reverse', store=False, readonly=True)
    x_force_print = fields.Boolean('Force Print')

    @api.depends_context('x_show_as_before')
    @api.depends('quantity', 'price_unit', 'price_subtotal', 'price_total')
    def _x_compute_reverse(self):
        for line in self:
            sign = -1

            if self._context.get('x_show_as_before'):
                sign *= -1

            line.x_quantity = sign * line.quantity
            line.x_price_subtotal = sign * line.price_subtotal
            line.x_price_total = sign * line.price_total

    @api.onchange('x_quantity', 'x_price_subtotal', 'x_price_total')
    def x_set_reverse_values(self):
        for line in self:
            line.quantity = -line.x_quantity
            line.price_subtotal = -line.x_price_subtotal
            line.price_total = -line.x_price_total

    def _convert_to_tax_line_dict(self):
        result = super()._convert_to_tax_line_dict()

        if self.env.company.x_use_ti:
            sign = self.move_id.move_type in ('out_refund',) and -1 or 1
            result['tax_amount'] *= sign
            result['tax_amount_local'] *= sign

        return result

    @api.depends('currency_id', 'company_id', 'move_id.date', 'move_id.x_currency_rate', 'move_id.x_invoice_sale_date')
    def _compute_currency_rate(self):
        super()._compute_currency_rate()

        if self.env.company.x_use_ti:
            for line_id in self.filtered(
                lambda rec: rec.move_id.x_show_currency_rate
                and rec.move_id.currency_id
                and not rec.move_id.currency_id.is_zero(rec.move_id.x_currency_rate)
                and rec.currency_id == rec.move_id.currency_id
            ):
                line_id.currency_rate = 1 / line_id.move_id.x_currency_rate

    def _stock_account_get_anglo_saxon_price_unit(self):
        # from stock_account
        # noinspection PyUnresolvedReferences
        price_unit = super()._stock_account_get_anglo_saxon_price_unit()

        # Fix of Odoo bug, applied to Polish companies' Credit Notes.
        # The first level of parent method has been used here as a fix (stock_account/models/account_move.py)
        if not self.move_id.x_use_ti or not self.sale_line_ids:
            return price_unit

        if not self.product_id:
            return self.price_unit

        original_line = fields.first(
            self.move_id.reversed_entry_id.line_ids.filtered(
                lambda _l: _l.display_type == 'cogs'
                and _l.product_id == self.product_id
                and _l.product_uom_id == self.product_uom_id
                and _l.currency_id == self.currency_id
                and float_compare(
                    _l.price_unit, 0.0, precision_digits=self.env['decimal.precision'].precision_get('Product Price')
                )
                >= 0
            )
        )

        return original_line.price_unit if original_line else price_unit

    def _eligible_for_cogs(self):
        # noinspection PyUnresolvedReferences
        res = super()._eligible_for_cogs()

        if (
            not res
            or self.move_type != 'out_refund'
            or not self.move_id.x_use_ti
            or not self._context.get('x_ti_additional_checks_eligible_for_cogs')
        ):
            return res

        # noinspection PyUnresolvedReferences
        return (
            # for matching invoice line from another site (x_is_corrected_line)
            # sum quantity of this line and self.quantity and check if it is zero
            not float_is_zero(
                sum(
                    self.move_id.invoice_line_ids.filtered(
                        lambda _l_id: _l_id.x_is_corrected_line is (not self.x_is_corrected_line)
                        and _l_id.product_id == self.product_id
                        and _l_id.product_uom_id == self.product_uom_id
                    ).mapped('quantity')
                )
                + self.quantity,
                precision_rounding=self.env['decimal.precision'].precision_get('Product Unit of Measure'),
            )
            and not self.move_id._stock_account_get_last_step_stock_moves()
        )

    def x_can_print(self):
        self.ensure_one()

        if not self.move_id.x_use_ti or not self.company_id.x_hide_zero_price_aml:
            return True

        return (
            self.x_force_print
            or self.display_type in ('line_section', 'line_note')
            or not self.currency_id.is_zero(self.price_unit)
        )
