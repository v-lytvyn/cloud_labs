from extensions import db
from my_project.auth.domain.patient import Patient

class PatientDAO:
    def get_all(self):
        return Patient.query.all()

    def get_by_id(self, id):
        return Patient.query.get(id)

    def create(self, patient):
        db.session.add(patient)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, patient):
        db.session.delete(patient)
        db.session.commit()
