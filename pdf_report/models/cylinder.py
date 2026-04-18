
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MRPCylinder(models.Model):
    _name = 'mrp.cylinder'

    name = fields.Char(string="Cylinder", required=True)
    mo_id = fields.Many2one("mrp.production", string="Manufacturing Order")
    product_id = fields.Many2one(related='mo_id.product_id')
    cylinder_qrcode = fields.Binary(string="QR Code")

    @api.onchange('name')
    def onchange_name(self):
        """
        Use: check the same serial number
        Added by: Jignesh
        Added on: 22/5/23
        Task:
        """
        self.ensure_one()
        if self.name:
            existing_cylinder = self.search([('name', 'ilike', self.name), ('product_id', '=', self.product_id.id)],
                                            limit=1)
            if existing_cylinder and self.name.lower().strip() == existing_cylinder.name.lower().strip():
                self.name = ''
                msg = _("{} cylinder serial number is already added!".format(existing_cylinder.name))
                return {'warning': {
                    'title': ("Warning for %s") % existing_cylinder.name,
                    'message': msg
                }}

    def generate_qr(self):
        if qrcode and base64:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=42,
                border=4,
            )
            product_name = (self.mo_id.product_id.name)
            valid_until = (self.mo_id.valid_date).date().strftime("%d/%m/%Y")
            cylinder_number  = (self.name)
            shelf_life = (self.mo_id.product_id.x_studio_shelf_life_months)
            sds_number = (self.mo_id.product_id.sds_number)
            multi_line_data = f"Product Name: {product_name}\n\nValid Until: {valid_until}\n\nCylinder Number: {cylinder_number}\n\nShelf Life (months): {shelf_life}\n\nSDS Number: {sds_number}"
            # Add data here to show while scanning the code
            qr.add_data(multi_line_data)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            self.write({'cylinder_qrcode': qr_image})
            return True
        else:
            raise UserError(
                _('Necessary Requirements To Run This Operation Is Not Satisfied'))
