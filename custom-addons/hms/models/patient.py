# models/patient.py
from odoo import models, fields

class Patient(models.Model):
    _name = "hms.patient"
    _description = "Patient"

    first_name = fields.Char()
    last_name = fields.Char()
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