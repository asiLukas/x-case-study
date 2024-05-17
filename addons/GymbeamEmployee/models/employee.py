from odoo import models, fields, api
import base64
import io
import pandas


class Employee(models.Model):
    _inherit = "hr.employee"

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

    @api.depends("salary", "tax")
    def _compute_total_salary(self):
        self.total_salary = self.salary + self.tax

    @api.model
    def write(self, vals):
        # NOTE there needs to be explicit check for False
        # NOTE the key can also be None when editing different fields
        if vals.get("special_phone") == False:
            vals["special_phone"] = "0901123456"
        return super(Employee, self).write(vals)
