from .utils import send_mail
from odoo import models, fields, api
from odoo.exceptions import UserError


class HrEmployeeEmailWizard(models.TransientModel):
    _name = "hr.employee.email.wizard"
    _description = "Wizard to Send Emails from Excel"

    employee_contacts = fields.Binary(string="Employee Contacts")

    def send_welcome_mails(self):
        if not self.employee_contacts:
            raise UserError("Please upload a valid .xlsx file.")

        send_mail(self.employee_contacts, self.env)
        return True
