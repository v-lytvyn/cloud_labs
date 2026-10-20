from extensions import db

class Service(db.Model):
    __tablename__ = 'Services'
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Service(id={self.service_id}, name='{self.name}')"