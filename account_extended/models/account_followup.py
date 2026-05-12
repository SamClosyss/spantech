from odoo import api, fields, models, _


class FollowupLine(models.Model):
    _inherit = 'account_followup.followup.line'

    # TODO: I think this field is no more in v16 and its non-use
    # Override this field because of change the default value
    description = fields.Text('Printed Message', translate=True, default=lambda s: _("""
    Unless we have made a mistake, it seems that the following invoice(s) marked as over-due remain unpaid, we would request that you take the appropriate measures to pay any overdue invoices in the next 5 days. 
    
    If your payment has already been made after this mail was sent, please ignore this message.
    Please do not hesitate to contact our accounting department with any question or query in relation to any of these invoices.
                
    Best Regards,
    Spantech UK Team
                """))


#     test push

