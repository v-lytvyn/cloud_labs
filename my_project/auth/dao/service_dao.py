from extensions import db
from my_project.auth.domain.service import Service

class ServiceDAO:
    def get_all(self):
        return Service.query.all()

    def get_by_id(self, id):
        return Service.query.get(id)

    def create(self, service):
        db.session.add(service)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self, service):
        db.session.delete(service)
        db.session.commit()