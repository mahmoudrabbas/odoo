from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    related_patient_id = fields.Many2one(
        "hms.patient",
        string="Related Patient",
    )

    @api.constrains('related_patient_id', 'email')
    def check_patient_email_conflict(self):
        """Block linking a customer whose email already exists in another patient."""
        for rec in self:
            if rec.related_patient_id and rec.email:
                conflict = self.env['hms.patient'].search([
                    ('email', '=', rec.email),
                    ('id', '!=', rec.related_patient_id.id),
                ], limit=1)
                if conflict:
                    raise ValidationError(
                        f"Cannot link: the email '{rec.email}' already belongs "
                        f"to patient {conflict.first_name} {conflict.last_name}."
                    )

    @api.constrains('vat', 'customer_rank')
    def check_vat_mandatory(self):
        """Tax ID is mandatory for CRM customers."""
        for rec in self:
            if (
                rec.customer_rank > 0
                and not rec.vat
                and not self.env.context.get('install_mode')
            ):
                raise ValidationError(
                    "Tax ID is mandatory for customers. "
                    f"Please fill it in for '{rec.name}'."
                )

    def unlink(self):
        for rec in self:
            if rec.related_patient_id:
                raise ValidationError(
                    f"Cannot delete '{rec.name}': this customer is linked to patient "
                    f"{rec.related_patient_id.first_name} {rec.related_patient_id.last_name}."
                )
        return super().unlink()