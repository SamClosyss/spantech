from odoo import api, fields, models, _


# https://spantech.odoo.com/web?debug=1#id=1002&menu_id=554&cids=7%2C4%2C3%2C2%2C1%2C6%2C8%2C5%2C10%2C9&action=806&model=project.task&view_type=form
class ProductComponents(models.Model):
    _name = 'product.components'

    component = fields.Char(string="Component", required=True)
    requested_value = fields.Char(string="Requested Value")
    accuracy = fields.Char(string="Accuracy")
    product_id = fields.Many2one("product.template", string="Product")

    def _prepare_order_line_values(self):
        self.ensure_one()
        return {'component': self.component,
                'requested_value': self.requested_value,
                'accuracy':self.accuracy
                }


class MrpComponents(models.Model):
    _name = 'mrp.components'

    component = fields.Char(string="Component", required=True)
    requested_value = fields.Char(string="Requested Value")
    accuracy = fields.Char(string="Accuracy")
    certified_value = fields.Char(string="Certified Value")
    mo_id = fields.Many2one("mrp.production", string="Manufacturing Order")
