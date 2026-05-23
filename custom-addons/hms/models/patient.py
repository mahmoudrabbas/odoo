from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = "hms.patient"
    _description = "Patient"

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)

    birth_date = fields.Date()

    history = fields.Html()

    cr_ratio = fields.Float()

    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O'),
    ])

    pcr = fields.Boolean()

    image = fields.Binary()

    address = fields.Text()

    age = fields.Integer()

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='undetermined')

    department_id = fields.Many2one("hms.department")

    department_capacity = fields.Integer(
        related="department_id.capacity"
    )

    doctor_ids = fields.Many2many("hms.doctor")

    log_ids = fields.One2many(
        "hms.patient.log",
        "patient_id"
    )

    @api.onchange('age')
    def onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'PCR checked automatically because age is less than 30'
                }
            }

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is mandatory when PCR is checked.")

    @api.constrains('department_id')
    def check_department_opened(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("You can't choose a closed department")

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.env['hms.patient.log'].create({
            'patient_id': res.id,
            'description': f"Patient created with state {res.state}"
        })
        return res

    def write(self, vals):
        old_state = self.state
        res = super().write(vals)
        if 'state' in vals:
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'description': f"State changed to {self.state}"
            })
        return res
