from odoo import api, models, fields
from odoo.exceptions import ValidationError


class GymbeamApplicant(models.Model):
    _inherit = "hr.applicant"

    applicant_number = fields.Char(
        string="Applicant Number", track_visibility="onchange", required=True
    )
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender"
    )

    @api.constrains("applicant_number")
    def check_for_uniqueness(self):
        if not self.applicant_number:
            return
        if (
            self.with_context(active_test=False).search_count(
                [
                    ("id", "!=", self.id),
                    ("applicant_number", "=", self.applicant_number),
                ]
            )
            > 0
            or self.env["hr.employee"]
            .with_context(active_test=False)
            .search_count([("employee_number", "=", self.applicant_number)])
            > 0
        ):
            # TODO maybe custom header
            raise ValidationError("Employee Number must be unique!")
