from odoo import models, fields, api
import base64
import io
import pandas
from odoo.exceptions import ValidationError


class GymbeamEmployee(models.Model):
    _inherit = "hr.employee"

    employee_number = fields.Char(
        string="Employee Number", track_visibility="onchange", required=True
    )
    i_love_gb = fields.Boolean(string="I Love GymBeam", default=True)
    salary = fields.Integer(string="Salary")
    tax = fields.Integer(string="Tax")
    total_salary = fields.Integer(
        string="Total Salary", compute="_compute_total_salary", store=True
    )
    special_phone = fields.Char(string="Special Phone")
    employee_contacts = fields.Binary(string="Employee Contacts")

    def send_welcome_mails(self):
        if self.employee_contacts:
            file_content = base64.b64decode(self.employee_contacts)

            pd_df = pandas.read_excel(io.BytesIO(file_content), header=None)

            for i, row in pd_df.iterrows():
                values = {
                    "email_to": row.iloc[0],
                    # "email_from": self.work_email,
                    "subject": row.iloc[1],
                    "body": "Welcome in GymBeam",
                }
                self.env["mail.mail"].sudo().create(values).send()

    def action_open_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Send Emails from Excel",
            "res_model": "hr.employee.email.wizard",
            "view_mode": "form",
            "target": "new",
        }

    # TODO main co delat priste, zajistit employee_number i na hr.applicant a aby byli unique
    # bude se jmenovat applicant_number ale taky bude unique s employee_number
    @api.constrains("employee_number")
    def check_for_uniqueness(self):
        if not self.employee_number:
            return
        if (
            self.search_count(
                [("id", "!=", self.id), ("employee_number", "=", self.employee_number)]
            )
            > 0
        ):
            # TODO maybe custom header
            raise ValidationError("Employee Number must be unique!")

    @api.depends("salary", "tax")
    def _compute_total_salary(self):
        self.total_salary = self.salary + self.tax

    def check_empty_field(self, vals, field, default_value) -> dict:
        if vals.get(field) == False:
            vals[field] = default_value
        return vals

    # TODO also replace mobile_phone??
    @api.model
    def write(self, vals):
        vals = self.check_empty_field(vals, "special_phone", "0901123456")
        return super(GymbeamEmployee, self).write(vals)

    @api.model
    def create(self, vals):
        vals = self.check_empty_field(vals, "special_phone", "0901123456")
        return super(GymbeamEmployee, self).create(vals)
