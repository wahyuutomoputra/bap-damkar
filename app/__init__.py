from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt
from app.controllers.user_controller import user_bp
from app.controllers.berita_acara_controller import berita_acara_bp
from app.controllers.auth_controller import auth_bp
from app.controllers.rescue_controller import rescue_bp
from app.controllers.report_controller import report_bp
from flask_swagger_ui import get_swaggerui_blueprint
from app.docs.berita_acara_docs import berita_acara_docs
from app.docs.user_docs import user_docs
from app.docs.rescue_docs import rescue_docs
from app.docs.report_docs import report_docs

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Simple CORS configuration
    CORS(app)
    

    # Swagger configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "BAP Damkar API Documentation"
        }
    )

    @app.route(API_URL)
    def swagger_api():
        swagger_config = {
            "openapi": "3.0.0",
            "info": {
                "title": "BAP Damkar API",
                "description": "API Documentation for Berita Acara Pemadaman Damkar",
                "version": "1.0.0"
            },
            "servers": [
                {
                    "url": "http://127.0.0.1:5000",
                    "description": "Development server"
                }
            ],
            "components": {
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            },
            "paths": {
                **berita_acara_docs,
                **user_docs,
                **rescue_docs,
                **report_docs
            }
        }
        return jsonify(swagger_config)

    # Register blueprints
    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(berita_acara_bp)
    app.register_blueprint(rescue_bp)
    app.register_blueprint(report_bp)

    return app 