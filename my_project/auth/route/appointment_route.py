import os
import json
import uuid
import boto3
import redis
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required
from my_project.auth.service.appointment_service import AppointmentService
from my_project.auth.controller.appointment_controller import AppointmentController

bp = Blueprint("appointments", __name__)
service = AppointmentService()
controller = AppointmentController()

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL = int(os.environ.get("CACHE_TTL", 45))
CACHE_ENABLED = os.environ.get("CACHE_ENABLED", "true").lower() == "true"
CACHE_KEY = "appointments:all"
IDEMPOTENCY_TTL = 86400  # 24 години

SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "")
AWS_REGION = os.environ.get("AWS_REGION", "eu-north-1")

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=1)
except Exception:
    redis_client = None

sqs_client = boto3.client("sqs", region_name=AWS_REGION) if SQS_QUEUE_URL else None


@bp.get("/")
def get_all():
    """
    Get all appointments (with Redis cache-aside)
    ---
    tags:
      - Appointments
    responses:
      200:
        description: Successfully retrieved list of appointments
    """
    if CACHE_ENABLED and redis_client is not None:
        try:
            cached_data = redis_client.get(CACHE_KEY)
            if cached_data is not None:
                redis_client.incr("cache:hits")
                resp = make_response(jsonify(json.loads(cached_data)), 200)
                resp.headers["X-Cache"] = "HIT"
                return resp
            redis_client.incr("cache:misses")
        except Exception:
            pass

    appts = service.get_all()
    result = [controller.convert(a) for a in appts]

    if CACHE_ENABLED and redis_client is not None:
        try:
            redis_client.setex(CACHE_KEY, CACHE_TTL, json.dumps(result))
        except Exception:
            pass

    resp = make_response(jsonify(result), 200)
    resp.headers["X-Cache"] = "MISS"
    return resp


@bp.get("/cache-stats")
def cache_stats():
    """
    Get Redis cache hit/miss statistics
    ---
    tags:
      - Appointments
    responses:
      200:
        description: Cache statistics
    """
    if redis_client is None:
        return jsonify({"error": "Redis not configured"}), 503
    try:
        hits = int(redis_client.get("cache:hits") or 0)
        misses = int(redis_client.get("cache:misses") or 0)
        total = hits + misses
        hit_ratio = round((hits / total) * 100, 2) if total > 0 else 0.0
        return jsonify({
            "hits": hits,
            "misses": misses,
            "total_reads": total,
            "hit_ratio_percent": hit_ratio
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    Create a new appointment (asynchronous via SQS with Idempotency-Key support)
    ---
    tags:
      - Appointments
    parameters:
      - name: Idempotency-Key
        in: header
        type: string
        required: false
        description: Unique key to guarantee idempotent request processing for 24 hours
      - in: body
        name: body
        schema:
          type: object
          properties:
            doctor_id:
              type: integer
              example: 1
            patient_id:
              type: integer
              example: 1
            appointment_datetime:
              type: string
              example: "2026-11-20 10:00:00"
            status:
              type: string
              example: "planned"
            notes:
              type: string
              example: "Consultation"
    responses:
      202:
        description: Appointment creation queued for asynchronous processing
      200:
        description: Appointment successfully created synchronously
      401:
        description: Unauthorized
    """
    idem_key = request.headers.get("Idempotency-Key")
    redis_idem_key = f"idempotency:{idem_key}" if idem_key else None

    if redis_idem_key and redis_client is not None:
        try:
            saved = redis_client.get(redis_idem_key)
            if saved is not None:
                parsed = json.loads(saved)
                resp = make_response(jsonify(parsed["body"]), parsed["status_code"])
                resp.headers["X-Idempotency-Replayed"] = "true"
                return resp
        except Exception:
            pass

    data = request.json or {}
    request_id = str(uuid.uuid4())

    if sqs_client is not None and SQS_QUEUE_URL:
        message_payload = {
            "request_id": request_id,
            "idempotency_key": idem_key,
            "data": data,
        }
        sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message_payload),
        )
        status_code = 202
        response_body = {
            "status": "accepted",
            "request_id": request_id,
            "idempotency_key": idem_key,
            "message": "Appointment creation queued for processing",
        }
    else:
        a = service.create(data)
        if redis_client is not None:
            try:
                redis_client.delete(CACHE_KEY)
            except Exception:
                pass
        status_code = 200
        response_body = controller.convert(a)

    if redis_idem_key and redis_client is not None:
        try:
            redis_client.setex(
                redis_idem_key,
                IDEMPOTENCY_TTL,
                json.dumps({"status_code": status_code, "body": response_body}),
            )
        except Exception:
            pass

    resp = make_response(jsonify(response_body), status_code)
    if idem_key:
        resp.headers["X-Idempotency-Replayed"] = "false"
    return resp


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
            appointment_datetime:
              type: string
              example: "2026-11-21 14:30:00"
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
