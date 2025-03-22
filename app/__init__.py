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

    # Disable strict slashes for all routes
    # app.url_map.strict_slashes = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Enable CORS for all routes
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Access-Control-Allow-Origin"],
            "supports_credentials": True
        }
    })

    # Add CORS headers to all responses
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Access-Control-Allow-Origin')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # Handle OPTIONS requests
    @app.route('/', methods=['OPTIONS'])
    def handle_options():
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Access-Control-Allow-Origin')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    

    # Swagger configuration
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
    
    # Create Swagger UI blueprint with minimal configuration
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "BAP Damkar API Documentation",
            'docExpansion': 'none',
            'defaultModelsExpandDepth': -1,
            'defaultModelExpandDepth': 1,
            'defaultModelRendering': 'model',
            'displayRequestDuration': True,
            'filter': True,
            'operationsSorter': 'alpha',
            'showExtensions': True,
            'showCommonExtensions': True,
            'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'options'],
            'tryItOutEnabled': True,
            'validatorUrl': None,
            'persistAuthorization': True,
            'deepLinking': True,
            'layout': "BaseLayout"
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
            "security": [],
            "paths": {
                **berita_acara_docs,
                **user_docs,
                **rescue_docs,
                **report_docs
            }
        }
        response = jsonify(swagger_config)
        return response

    # Register blueprints
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(berita_acara_bp)
    app.register_blueprint(rescue_bp)
    app.register_blueprint(report_bp)

    return app 