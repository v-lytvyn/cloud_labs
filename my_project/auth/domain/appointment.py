from extensions import db

class Appointment(db.Model):
    __tablename__ = "Appointments"

    appointment_id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("Doctors.doctor_id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("Patients.patient_id"), nullable=False)
    appointment_datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('planned','completed','cancelled','no_show'))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    doctor = db.relationship("Doctor")
    patient = db.relationship("Patient")
