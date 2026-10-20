from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from my_project.auth.service.doctor_service import DoctorService
from my_project.auth.controller.doctor_controller import DoctorController

bp = Blueprint("doctors", __name__)
service = DoctorService()
controller = DoctorController()

@bp.get("/")
def get_all():
    """
    Get all doctors
    ---
    tags:
      - Doctors
    responses:
      200:
        description: Successfully retrieved list of doctors
    """
    doctors = service.get_all()
    return [controller.convert(d) for d in doctors]

@bp.get("/<int:id>")
def get_by_id(id):
    """
    Get a doctor by ID
    ---
    tags:
      - Doctors
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Doctor ID
    responses:
      200:
        description: Doctor data
    """
    d = service.get(id)
    return controller.convert(d)

@bp.post("/")
@jwt_required()
def create():
    """
    Create a new doctor
    ---
    tags:
      - Doctors
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            first_name:
              type: string
              example: "John"
            last_name:
              type: string
              example: "Doe"
            specialization:
              type: string
              example: "Surgeon"
            phone:
              type: string
              example: "+380501234567"
            email:
              type: string
              example: "doctor@hospital.com"
    responses:
      200:
        description: Doctor successfully created
      401:
        description: Unauthorized
    """
    data = request.json
    d = service.create(data)
    return controller.convert(d)

@bp.put("/<int:id>")
@jwt_required()
def update(id):
    """
    Update doctor data
    ---
    tags:
      - Doctors
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Doctor ID
      - in: body
        name: body
        schema:
          type: object
          properties:
            specialization:
              type: string
              example: "Head Surgeon"
            phone:
              type: string
              example: "+380507654321"
    responses:
      200:
        description: Doctor data updated
      401:
        description: Unauthorized
    """
    data = request.json
    d = service.update(id, data)
    return controller.convert(d)

@bp.delete("/<int:id>")
@jwt_required()
def delete(id):
    """
    Delete a doctor
    ---
    tags:
      - Doctors
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Doctor ID
    responses:
      200:
        description: Doctor deleted
      401:
        description: Unauthorized
    """
    service.delete(id)
    return {"status": "deleted"}
