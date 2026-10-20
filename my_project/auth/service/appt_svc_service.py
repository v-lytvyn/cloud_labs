from my_project.auth.dao.appt_svc_dao import ApptServiceDAO
from my_project.auth.domain.appt_svc import AppointmentService

class ApptServiceService:
    def __init__(self):
        self.dao = ApptServiceDAO()

    def get_all(self):
        return self.dao.get_all()

    def get_for_appointment(self, appt_id):
        return self.dao.get_for_appointment(appt_id)

    def add(self, data):
        obj = AppointmentService(**data)
        self.dao.add(obj)
        return obj

    def delete(self, appt_id, service_id):
        obj = AppointmentService.query.get((appt_id, service_id))
        self.dao.delete(obj)
