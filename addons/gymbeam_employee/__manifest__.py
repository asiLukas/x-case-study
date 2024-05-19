{
    "name": "Gymbeam Employee",
    "version": "1.0",
    "summary": "Custom Employee addon",
    "description": "This module extends the built-in Employee app",
    "author": "luky",
    "website": "https://www.odoo.com/app/employees",
    "depends": ["hr"],
    "data": [
        "views/gymbeam_employee_view.xml",
        "views/mail_wizard_view.xml",
        "views/job_position_view.xml",
        "data/mail_wizard_data.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": True,
}
