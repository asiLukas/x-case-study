from odoo import models, fields

class Test(models.Model):
    _name = 'my.test'
    _description = 'My Test'

    name = fields.Char(string='Name', required=True)
