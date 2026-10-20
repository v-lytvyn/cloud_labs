from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from my_project.auth.service.patient_service import PatientService
from my_project.auth.controller.patient_controller import PatientController

bp = Blueprint("patients", __name__)
service = PatientService()
controller = PatientController()

@bp.get("/")
def get_all():
    """
    Get all patients
    ---
    tags:
      - Patients
    responses:
      200:
        description: Successfully retrieved list of patients
    """
    patients = service.get_all()
    return [controller.convert(p) for p in patients]

@bp.get("/<int:id>")
def get_by_id(id):
    """
    Get a patient by ID
    ---
    tags:
      - Patients
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Patient ID
    responses:
      200:
        description: Patient data
    """
    p = service.get(id)
    return controller.convert(p)

@bp.post("/")
@jwt_required()
def create():
    """
    Create a new patient
    ---
    tags:
      - Patients
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            first_name:
              type: string
              example: "Jane"
            last_name:
              type: string
              example: "Doe"
            phone:
              type: string
              example: "+380671234567"
            email:
              type: string
              example: "jane.doe@example.com"
    responses:
      200:
        description: Patient successfully created
      401:
        description: Unauthorized
    """
    data = request.json
    p = service.create(data)
    return controller.convert(p)

@bp.put("/<int:id>")
@jwt_required()
def update(id):
    """
    Update patient data
    ---
    tags:
      - Patients
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Patient ID
      - in: body
        name: body
        schema:
          type: object
          properties:
            phone:
              type: string
              example: "+380679876543"
            email:
              type: string
              example: "new.email@example.com"
    responses:
      200:
        description: Patient data updated
      401:
        description: Unauthorized
    """
    data = request.json
    p = service.update(id, data)
    return controller.convert(p)

@bp.delete("/<int:id>")
@jwt_required()
def delete(id):
    """
    Delete a patient
    ---
    tags:
      - Patients
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Patient ID
    responses:
      200:
        description: Patient deleted
      401:
        description: Unauthorized
    """
    service.delete(id)
    return {"status": "deleted"}
