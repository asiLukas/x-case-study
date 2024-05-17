from odoo import models, fields, api


class Employee(models.Model):
    _inherit = "hr.employee"

    i_love_gb = fields.Boolean(string="I Love GymBeam", default=True)
    salary = fields.Integer(string="Salary")
    tax = fields.Integer(string="Tax")
    total_salary = fields.Integer(
        string="Total Salary", compute="_compute_total_salary", store=True
    )

    @api.depends("salary", "tax")
    def _compute_total_salary(self):
        self.total_salary = self.salary + self.tax

    @api.model
    def create(self, vals):
        # Add custom logic here
        return super(Employee, self).create(vals)
