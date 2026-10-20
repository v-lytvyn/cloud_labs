from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import text
from extensions import db

bp = Blueprint('lab5', __name__)

@bp.route('/generate-dummies', methods=['POST'])
@jwt_required()
def generate_dummies():
    """
    Generate dummy patients using a stored procedure
    ---
    tags:
      - Lab Procedures
    responses:
      201:
        description: 10 dummy patients inserted successfully
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    try:
        db.session.execute(text("CALL sp_insert_dummy_patients()"))
        db.session.commit()
        return jsonify({"message": "10 dummy patients inserted successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/split-tables', methods=['POST'])
@jwt_required()
def split_tables():
    """
    Split patient tables dynamically using a cursor
    ---
    tags:
      - Lab Procedures
    responses:
      200:
        description: Tables split dynamically using cursor
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    try:
        db.session.execute(text("CALL sp_cursor_split_patients()"))
        db.session.commit()
        return jsonify({"message": "Tables split dynamically using cursor"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/add-note', methods=['POST'])
@jwt_required()
def add_note():
    """
    Add a note for a patient
    ---
    tags:
      - Lab Procedures
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            patient_id:
              type: integer
              example: 1
            note:
              type: string
              example: "Patient complains of headache."
    responses:
      201:
        description: Note added successfully
      400:
        description: Trigger error or bad request
      401:
        description: Unauthorized
    """
    data = request.json
    try:
        sql = text("INSERT INTO Patient_Notes (patient_id, note_text) VALUES (:pid, :txt)")
        db.session.execute(sql, {"pid": data.get('patient_id'), "txt": data.get('note')})
        db.session.commit()
        return jsonify({"message": "Note added"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"trigger_error": str(e)}), 400

@bp.route('/create-appt-by-name', methods=['POST'])
@jwt_required()
def create_appt_by_name():
    """
    Create an appointment using doctor and patient surnames
    ---
    tags:
      - Lab Procedures
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            doc_surname:
              type: string
              example: "Doe"
            pat_surname:
              type: string
              example: "Smith"
            date:
              type: string
              example: "2026-12-01T10:00:00"
    responses:
      201:
        description: Appointment created via stored procedure
      400:
        description: Bad request
      401:
        description: Unauthorized
    """
    data = request.json
    try:
        sql = text("CALL sp_create_appointment_by_names(:dname, :pname, :date)")
        db.session.execute(sql, {
            "dname": data.get('doc_surname'),
            "pname": data.get('pat_surname'),
            "date": data.get('date')
        })
        db.session.commit()
        return jsonify({"message": "Appointment created via stored procedure"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@bp.route('/appt-totals', methods=['GET'])
@jwt_required()
def get_totals():
    """
    Get appointment totals
    ---
    tags:
      - Lab Procedures
    responses:
      200:
        description: Successfully retrieved appointment totals
      401:
        description: Unauthorized
      500:
        description: Internal server error
    """
    try:
        result = db.session.execute(text("CALL sp_show_appointment_totals()")).fetchall()
        data = [{"appointment_id": row[0], "total_paid": float(row[1])} for row in result]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/add-service', methods=['POST'])
@jwt_required()
def add_service():
    """
    Add a new service via stored procedure
    ---
    tags:
      - Lab Procedures
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Ultrasound"
            description:
              type: string
              example: "Abdominal ultrasound scan"
            price:
              type: number
              format: float
              example: 150.00
    responses:
      201:
        description: Service added successfully via Stored Procedure
      400:
        description: Bad request
      401:
        description: Unauthorized
    """
    data = request.json
    try:
        sql = text("CALL sp_add_service(:p_name, :p_desc, :p_price)")
        
        db.session.execute(sql, {
            "p_name": data.get('name'),
            "p_desc": data.get('description'),
            "p_price": data.get('price')
        })
        db.session.commit()
        return jsonify({"message": "Service added successfully via Stored Procedure"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
