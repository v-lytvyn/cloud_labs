from my_project.auth.dao.service_dao import ServiceDAO
from my_project.auth.domain.service import Service

class ServiceService:
    def __init__(self):
        self.dao = ServiceDAO()

    def get_all(self):
        return self.dao.get_all()

    def get(self, id):
        return self.dao.get_by_id(id)

    def create(self, data):
        new_service = Service(**data)
        self.dao.create(new_service)
        return new_service

    def update(self, id, data):
        service = self.dao.get_by_id(id)
        if service:
            for key, value in data.items():
                setattr(service, key, value) 
            self.dao.update()
            return service
        return None

    def delete(self, id):
        service = self.dao.get_by_id(id)
        if service:
            self.dao.delete(service)
            return True
        return False