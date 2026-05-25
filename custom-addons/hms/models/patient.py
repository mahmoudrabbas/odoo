from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re


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

    email = fields.Char(string="Email")

    age = fields.Integer(compute='_compute_age', store=True)

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


    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = (
                    today.year - rec.birth_date.year
                    - ((today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
                )
            else:
                rec.age = 0


    @api.onchange('birth_date')
    def onchange_birth_date(self):
        if self.birth_date:
            today = date.today()
            age = (
                today.year - self.birth_date.year
                - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            )
            if age < 30:
                self.pcr = True
                return {
                    'warning': {
                        'title': 'Warning',
                        'message': 'PCR checked automatically because age is less than 30',
                    }
                }


    @api.constrains('email')
    def check_email_format(self):
        pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        for rec in self:
            if rec.email and not re.match(pattern, rec.email):
                raise ValidationError(f"'{rec.email}' is not a valid email address.")

    @api.constrains('email')
    def _check_unique_email(self):
        for rec in self:
            if rec.email:
                duplicate = self.search([
                    ('email', '=', rec.email),
                    ('id', '!=', rec.id),
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        f"The email '{rec.email}' is already used by another patient."
                    )

    @api.constrains('pcr', 'cr_ratio')
    def check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is mandatory when PCR is checked.")

    @api.constrains('department_id')
    def check_department_opened(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("You can't choose a closed department.")


    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.env['hms.patient.log'].create({
            'patient_id': res.id,
            'description': f"Patient created with state {res.state}",
        })
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'state' in vals:
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'description': f"State changed to {self.state}",
            })
        return res