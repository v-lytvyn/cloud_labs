import os
import yaml
from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from extensions import db

from my_project.auth.route.patient_route import bp as patient_bp
from my_project.auth.route.doctor_route import bp as doctor_bp
from my_project.auth.route.appointment_route import bp as appointment_bp
from my_project.auth.route.appt_svc_route import bp as appt_service_bp
from my_project.auth.route.service_route import bp as service_bp
from my_project.auth.route.lab_route import bp as lab_bp
from my_project.auth.route.login_route import bp as login_bp

def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "super-secret-lab-key-2026" 
    jwt = JWTManager(app)

    swagger_template = {
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter your token in the format: Bearer <your_token>"
            }
        },
        "security": [
            {"Bearer": []}
        ]
    }
    
    swagger = Swagger(app, template=swagger_template)

    config = yaml.safe_load(open("config/app.yml"))
    db_url = os.environ.get("DATABASE_URL") or config["database"]["url"]

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(patient_bp, url_prefix="/patients")
    app.register_blueprint(doctor_bp, url_prefix="/doctors")
    app.register_blueprint(appointment_bp, url_prefix="/appointments")
    app.register_blueprint(appt_service_bp, url_prefix="/appointment-services")
    app.register_blueprint(service_bp, url_prefix="/services")
    app.register_blueprint(lab_bp, url_prefix="/lab5")
    app.register_blueprint(login_bp, url_prefix="/auth")

    return app

app = create_app()

with app.app_context():
    db.create_all()

@app.route('/health')
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
