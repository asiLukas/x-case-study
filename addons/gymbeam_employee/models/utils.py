import base64
import io
import pandas

from odoo.exceptions import ValidationError


def send_mail(employee_contacts, env) -> None:
    """
    creates and sends welcome mails to the recipients
    supplied in an excel file in the self.employee_contacts

    :param empoyee_contacts(bytes): the excel file
    :param env: the environment of 'hr.employee'
    """

    file_content = base64.b64decode(employee_contacts)

    try:
        pd_df = pandas.read_excel(io.BytesIO(file_content), header=None)
    except ValueError:
        raise ValidationError("Please upload a valid .xlsx or .xls file")

    for _, row in pd_df.iterrows():
        values = {
            "email_to": row.iloc[0],
            # "email_from": self.work_email,
            "subject": row.iloc[1],
            "body_html": "<h1>Welcome in GymBeam<h1/>",
        }
        env["mail.mail"].sudo().create(values).send()
