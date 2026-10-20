class AppointmentController:
    def convert(self, a):
        return {
            "appointment_id": a.appointment_id,
            "doctor": {
                "doctor_id": a.doctor.doctor_id,
                "first_name": a.doctor.first_name,
                "last_name": a.doctor.last_name,
            },
            "patient": {
                "patient_id": a.patient.patient_id,
                "first_name": a.patient.first_name,
                "last_name": a.patient.last_name,
            },
            "appointment_datetime": str(a.appointment_datetime),
            "status": a.status,
            "notes": a.notes
        }
