import uuid
import json

from odoo import http
from odoo.http import request, Response


class GymbeamApplicantController(http.Controller):
    @http.route(
        "/case_study/applicant/get", type="json", auth="public", methods=["POST"]
    )
    def create_applicant_bulk(self):
        data = request.get_json_data()

        if not (candidates := data.pop("candidates", None)):
            return Response("Missing required field 'candidates'", status=400)
        if not isinstance(candidates, list):
            return Response(
                "The field 'candidates' should be an array or a list", status=400
            )

        applicant_ids = []
        for candidate in candidates:
            name = f'{candidate.pop("firstname", "")} {candidate.pop("surname", "")}'
            phone = candidate.pop("phone", None)
            email = candidate.pop("email", None)
            gender = candidate.pop("gender", None)
            if not isinstance((job := candidate.pop("job", None)), dict):
                return Response("Missing or invalid 'job' field")
            api_id = job.get("id", None)

            if not all([name, phone, email, gender, api_id]):
                return Response("Missing required fields", status=400)

            job_position = (
                request.env["hr.job"].sudo().search([("api_id", "=", api_id)], limit=1)
            )
            if not job_position:
                job_position = (
                    request.env["hr.job"]
                    .sudo()
                    .create({"name": job.get("title"), "api_id": api_id})
                )

            applicant_ids.append(
                request.env["hr.applicant"]
                .sudo()
                .create(
                    {
                        "name": name,
                        "partner_name": name,
                        "partner_phone": phone,
                        "email_from": email,
                        "gender": gender,
                        "job_id": job_position.id,
                        "applicant_number": candidate.pop("applicant_number", None)
                        or uuid.uuid4(),
                    }
                )
                .id
            )

        return Response(
            json.dumps({"applicant_ids": applicant_ids}),
            status=200,
            content_type="application/json",
        )
