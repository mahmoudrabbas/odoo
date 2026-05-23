from odoo import models, fields

class Doctor(models.Model):
    _name = "hms.doctor"
    _description = "Doctor"

    first_name = fields.Char(required=True)

    last_name = fields.Char(required=True)

    image = fields.Binary()

    department_id = fields.Many2one(
        "hms.department"
    )
