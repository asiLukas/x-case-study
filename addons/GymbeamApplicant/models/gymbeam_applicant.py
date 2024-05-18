from odoo import api, models, fields


class GymbeamApplicant(models.Model):
    _inherit = "hr.applicant"

    applicant_number = fields.Char(
        string="Applicant Number", track_visibility="onchange", required=True
    )
