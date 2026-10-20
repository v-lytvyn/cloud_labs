from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from my_project.auth.service.service_service import ServiceService
from my_project.auth.controller.service_controller import ServiceController

bp = Blueprint("services", __name__)
service = ServiceService()
controller = ServiceController()

@bp.get("/")
def get_all():
    """
    Get all services
    ---
    tags:
      - Services
    responses:
      200:
        description: Successfully retrieved list of services
    """
    services = service.get_all()
    return [controller.convert(s) for s in services]

@bp.get("/<int:id>")
def get_by_id(id):
    """
    Get a service by ID
    ---
    tags:
      - Services
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Service ID
    responses:
      200:
        description: Service data
    """
    s = service.get(id)
    return controller.convert(s)

@bp.post("/")
@jwt_required()
def create():
    """
    Create a new service
    ---
    tags:
      - Services
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Blood Test"
            description:
              type: string
              example: "General blood analysis"
            price:
              type: number
              format: float
              example: 50.00
    responses:
      200:
        description: Service successfully created
      401:
        description: Unauthorized
    """
    data = request.json
    s = service.create(data)
    return controller.convert(s)

@bp.put("/<int:id>")
@jwt_required()
def update(id):
    """
    Update service data
    ---
    tags:
      - Services
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Service ID
      - in: body
        name: body
        schema:
          type: object
          properties:
            price:
              type: number
              format: float
              example: 60.00
            description:
              type: string
              example: "Advanced blood analysis"
    responses:
      200:
        description: Service data updated
      401:
        description: Unauthorized
    """
    data = request.json
    s = service.update(id, data)
    return controller.convert(s)

@bp.delete("/<int:id>")
@jwt_required()
def delete(id):
    """
    Delete a service
    ---
    tags:
      - Services
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: Service ID
    responses:
      200:
        description: Service deleted
      401:
        description: Unauthorized
    """
    service.delete(id)
    return {"status": "deleted"}
