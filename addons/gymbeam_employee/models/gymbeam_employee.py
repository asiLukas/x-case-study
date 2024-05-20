from .utils import send_mail

from odoo import models, fields, api
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

    def send_welcome_mails(self) -> None:
        """creates and sends welcome mails to the recipients
        supplied in an excel file in the self.employee_contacts"""

        if self.employee_contacts:
            send_mail(self.employee_contacts, self.env)

    def action_open_wizard(self) -> dict:
        """action to open a wizard windows"""

        return {
            "type": "ir.actions.act_window",
            "name": "Send Emails from Excel",
            "res_model": "hr.employee.email.wizard",
            "view_mode": "form",
            "target": "new",
        }

    @api.constrains("employee_number")
    def check_for_uniqueness(self) -> None:
        """checks if both employee_number and applicant_number are unique between each other"""

        if not self.employee_number:
            return
        if (
            self.with_context(active_test=False).search_count(
                [("id", "!=", self.id), ("employee_number", "=", self.employee_number)]
            )
            > 0
            or self.with_context(active_test=False)
            .env["hr.applicant"]
            .search_count([("applicant_number", "=", self.employee_number)])
            > 0
        ):
            raise ValidationError("Employee Number must be unique!")

    @api.depends("salary", "tax")
    def _compute_total_salary(self) -> None:
        self.total_salary = self.salary + self.tax

    def check_empty_field(self, vals, field, default_value) -> dict:
        """
        checks if a field is not filled in

        :param vals(dict): the dict of fields to check
        :param field(str):  the field to check in the dict
        :param default_value(str): the default value that should be set when the field is empty
        :returns vals(dict): the new updated vals dict
        """
        if vals.get(field) == False:
            vals[field] = default_value
        return vals

    @api.model
    def write(self, vals):
        vals = self.check_empty_field(vals, "special_phone", "0901123456")
        return super(GymbeamEmployee, self).write(vals)

    @api.model
    def create(self, vals):
        vals = self.check_empty_field(vals, "special_phone", "0901123456")
        return super(GymbeamEmployee, self).create(vals)
