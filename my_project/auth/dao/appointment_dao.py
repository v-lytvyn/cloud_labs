from extensions import db
from my_project.auth.domain.appointment import Appointment

class AppointmentDAO:
    def get_all(self):
        return Appointment.query.all()

    def get_by_id(self, id):
        return Appointment.query.get(id)

    def create(self, appt):
        db.session.add(appt)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, appt):
        db.session.delete(appt)
        db.session.commit()

    def get_by_doctor(self, doctor_id):
        return Appointment.query.filter_by(doctor_id=doctor_id).all()

    def get_by_patient(self, patient_id):
        return Appointment.query.filter_by(patient_id=patient_id).all()
