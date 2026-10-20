from extensions import db
from my_project.auth.domain.appointment import Appointment 
from my_project.auth.domain.service import Service 

class AppointmentService(db.Model):
    __tablename__ = "Appointment_Services"

    appointment_id = db.Column(db.Integer, db.ForeignKey("Appointments.appointment_id"), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey("Services.service_id"), primary_key=True)
    quantity = db.Column(db.Integer, default=1)

    appointment = db.relationship("Appointment", backref="appt_services_ref")
    service = db.relationship("Service", backref="appt_services_ref") 
