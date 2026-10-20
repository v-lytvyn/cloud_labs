from my_project.auth.dao.appointment_dao import AppointmentDAO
from my_project.auth.domain.appointment import Appointment

class AppointmentService:
    def __init__(self):
        self.dao = AppointmentDAO()

    def get_all(self):
        return self.dao.get_all()

    def get(self, id):
        return self.dao.get_by_id(id)

    def create(self, data):
        appt = Appointment(**data)
        self.dao.create(appt)
        return appt

    def update(self, id, data):
        a = self.dao.get_by_id(id)
        for key, value in data.items():
            setattr(a, key, value)
        self.dao.update()
        return a

    def delete(self, id):
        a = self.dao.get_by_id(id)
        self.dao.delete(a)

    def get_for_doctor(self, doctor_id):
        return self.dao.get_by_doctor(doctor_id)

    def get_for_patient(self, patient_id):
        return self.dao.get_by_patient(patient_id)
