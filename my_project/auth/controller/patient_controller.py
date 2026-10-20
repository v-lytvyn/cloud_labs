class PatientController:
    def convert(self, p):
        return {
            "patient_id": p.patient_id,
            "first_name": p.first_name,
            "last_name": p.last_name,
            "birth_date": str(p.birth_date) if p.birth_date else None,
            "gender": p.gender,
            "phone": p.phone,
            "email": p.email,
            "address": p.address
        }
