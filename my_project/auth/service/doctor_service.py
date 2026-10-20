from my_project.auth.dao.doctor_dao import DoctorDAO
from my_project.auth.domain.doctor import Doctor

class DoctorService:
    def __init__(self):
        self.dao = DoctorDAO()

    def get_all(self):
        return self.dao.get_all()

    def get(self, id):
        return self.dao.get_by_id(id)

    def create(self, data):
        doctor = Doctor(**data)
        self.dao.create(doctor)
        return doctor

    def update(self, id, data):
        d = self.dao.get_by_id(id)
        for key, value in data.items():
            setattr(d, key, value)
        self.dao.update()
        return d

    def delete(self, id):
        d = self.dao.get_by_id(id)
        self.dao.delete(d)
