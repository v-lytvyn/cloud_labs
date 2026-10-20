class DoctorController:
    def convert(self, d):
        return {
            "doctor_id": d.doctor_id,
            "first_name": d.first_name,
            "last_name": d.last_name,
            "specialization": d.specialization,
            "phone": d.phone,
            "email": d.email
        }
