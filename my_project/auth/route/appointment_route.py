from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from my_project.auth.service.appointment_service import AppointmentService
from my_project.auth.controller.appointment_controller import AppointmentController

bp = Blueprint("appointments", __name__)
service = AppointmentService()
controller = AppointmentController()

@bp.get("/")
def get_all():
    """
    Get all appointments
    ---
    tags:
      - Appointments
    responses:
      200:
        description: Successfully retrieved list of appointments
    """
    appts = service.get_all()
    return [controller.convert(a) for a in appts]

@bp.get("/<int:id>")
def get_by_id(id):
    """
    Get appointment by ID
    ---
    tags:
      - Appointments
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Appointment ID
    responses:
      200:
        description: Appointment data
    """
    a = service.get(id)
    return controller.convert(a)

@bp.post("/")
@jwt_required()
def create():
    """
    Create a new appointment
    ---
    tags:
      - Appointments
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            date:
              type: string
              example: "2026-11-20T10:00:00"
            doctor_id:
              type: integer
              example: 1
            patient_id:
              type: integer
              example: 1
    responses:
      200:
        description: Appointment successfully created
      401:
        description: Unauthorized
    """
    data = request.json
    a = service.create(data)
    return controller.convert(a)

@bp.put("/<int:id>")
@jwt_required()
def update(id):
    """
    Update appointment data
    ---
    tags:
      - Appointments
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            date:
              type: string
              example: "2026-11-21T14:30:00"
    responses:
      200:
        description: Appointment data updated
      401:
        description: Unauthorized
    """
    data = request.json
    a = service.update(id, data)
    return controller.convert(a)

@bp.delete("/<int:id>")
@jwt_required()
def delete(id):
    """
    Delete an appointment
    ---
    tags:
      - Appointments
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Appointment deleted
      401:
        description: Unauthorized
    """
    service.delete(id)
    return {"status": "deleted"}

@bp.get("/doctor/<int:doctor_id>")
def get_by_doctor(doctor_id):
    """
    Get appointments by doctor ID
    ---
    tags:
      - Appointments
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
        description: Doctor ID
    responses:
      200:
        description: List of appointments for the specific doctor
    """
    appts = service.get_for_doctor(doctor_id)
    return [controller.convert(a) for a in appts]

@bp.get("/patient/<int:patient_id>")
def get_by_patient(patient_id):
    """
    Get appointments by patient ID
    ---
    tags:
      - Appointments
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: Patient ID
    responses:
      200:
        description: List of appointments for the specific patient
    """
    appts = service.get_for_patient(patient_id)
    return [controller.convert(a) for a in appts]
