class ServiceController:
    def convert(self, s):
        return {
            "service_id": s.service_id,
            "name": s.name,
            "price": str(s.price), 
            "description": s.description
        }