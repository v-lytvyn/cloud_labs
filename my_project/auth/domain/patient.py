from extensions import db

class Patient(db.Model):
    __tablename__ = "Patients"

    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.Enum('M', 'F'))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime)
