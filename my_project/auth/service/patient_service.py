from my_project.auth.dao.patient_dao import PatientDAO
from my_project.auth.domain.patient import Patient

class PatientService:
    def __init__(self):
        self.dao = PatientDAO()

    def get_all(self):
        return self.dao.get_all()

    def get(self, id):
        return self.dao.get_by_id(id)

    def create(self, data):
        patient = Patient(**data)
        self.dao.create(patient)
        return patient

    def update(self, id, data):
        p = self.dao.get_by_id(id)
        for key, value in data.items():
            setattr(p, key, value)
        self.dao.update()
        return p

    def delete(self, id):
        p = self.dao.get_by_id(id)
        self.dao.delete(p)
