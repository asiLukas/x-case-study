from odoo import models, fields, api
import base64
import io
import pandas
from odoo.exceptions import UserError


class HrEmployeeEmailWizard(models.TransientModel):
    _name = "hr.employee.email.wizard"
    _description = "Wizard to Send Emails from Excel"

    employee_contacts = fields.Binary(string="Employee Contacts")

    def send_welcome_mails(self):
        if not self.employee_contacts:
            raise UserError("Please upload a valid .xlsx file.")

        file_content = base64.b64decode(self.employee_contacts)
        # NOTE for testing
        print(file_content)

        pd_df = pandas.read_excel(io.BytesIO(file_content), header=None)

        for i, row in pd_df.iterrows():
            values = {
                "email_to": row.iloc[0],
                # "email_from": self.work_email,
                "subject": row.iloc[1],
                "body": "Welcome in GymBeam",
            }
            # NOTE for testing
            print(values)
            self.env["mail.mail"].sudo().create(values).send()

        return True
