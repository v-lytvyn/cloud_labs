from extensions import db
from my_project.auth.domain.doctor import Doctor

class DoctorDAO:
    def get_all(self):
        return Doctor.query.all()

    def get_by_id(self, id):
        return Doctor.query.get(id)

    def create(self, doctor):
        db.session.add(doctor)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, doctor):
        db.session.delete(doctor)
        db.session.commit()
