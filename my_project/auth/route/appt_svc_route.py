from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from my_project.auth.service.appt_svc_service import ApptServiceService
from my_project.auth.controller.appt_svc_controller import ApptServiceController

bp = Blueprint("appointment_services", __name__)
service = ApptServiceService()
controller = ApptServiceController()

@bp.get("/")
def get_all():
    """
    Get all appointment services
    ---
    tags:
      - Appointment Services
    responses:
      200:
        description: Successfully retrieved list of appointment services
    """
    items = service.get_all()
    return [controller.convert(i) for i in items]

@bp.get("/<int:appt_id>")
def get_for_appointment(appt_id):
    """
    Get services for a specific appointment
    ---
    tags:
      - Appointment Services
    parameters:
      - name: appt_id
        in: path
        type: integer
        required: true
        description: Appointment ID
    responses:
      200:
        description: List of services for the appointment
    """
    items = service.get_for_appointment(appt_id)
    return [controller.convert(i) for i in items]

@bp.post("/")
@jwt_required()
def add():
    """
    Add a service to an appointment
    ---
    tags:
      - Appointment Services
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
              example: 1
            service_id:
              type: integer
              example: 1
    responses:
      200:
        description: Service successfully added to appointment
      401:
        description: Unauthorized
    """
    data = request.json
    obj = service.add(data)
    return controller.convert(obj)

@bp.delete("/<int:appt_id>/<int:service_id>")
@jwt_required()
def delete(appt_id, service_id):
    """
    Remove a service from an appointment
    ---
    tags:
      - Appointment Services
    parameters:
      - name: appt_id
        in: path
        type: integer
        required: true
        description: Appointment ID
      - name: service_id
        in: path
        type: integer
        required: true
        description: Service ID
    responses:
      200:
        description: Service successfully removed from appointment
      401:
        description: Unauthorized
    """
    service.delete(appt_id, service_id)
    return {"status": "deleted"}
