from extensions import db
from my_project.auth.domain.appt_svc import AppointmentService

class ApptServiceDAO:
    def get_all(self):
        return AppointmentService.query.all()

    def get_for_appointment(self, appt_id):
        return AppointmentService.query.filter_by(appointment_id=appt_id).all()

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
