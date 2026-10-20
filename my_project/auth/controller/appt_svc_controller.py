class ApptServiceController:
    def convert(self, a):
        return {
            "quantity": a.quantity,
            
            "appointment_info": {
                "appointment_id": a.appointment.appointment_id,
                "datetime": str(a.appointment.appointment_datetime),
            },
            
            "service_info": {
                "service_id": a.service.service_id,
                "name": a.service.name,
                "price": str(a.service.price),
            }
        }