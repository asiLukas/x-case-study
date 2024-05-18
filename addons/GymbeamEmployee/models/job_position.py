from odoo import api, fields, models


class JobPosition(models.Model):
    _inherit = "hr.job"

    api_id = fields.Integer(string="API ID", required=True)

    _sql_constraints = [
        ("ref_unique", "unique(api_id)", "API ID should be unique!"),
    ]
