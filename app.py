from flask import Flask
from flask_cors import CORS
from config_app.jwt_config import configure_jwt
from routes import auth_routes , cliente_routes,suscripcion_routes,dashboard_routes,empresa_routes

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    configure_jwt(app)
    app.register_blueprint(auth_routes.auth_bp, url_prefix='/api')
    app.register_blueprint(cliente_routes.cliente_bp, url_prefix='/api/cliente')  
    app.register_blueprint(suscripcion_routes.suscripcion_bp,url_prefix='/api/suscripcion')
    app.register_blueprint(dashboard_routes.dashboard_bp,url_prefix='/api/dashboard')
    app.register_blueprint(empresa_routes.empresa_bp,url_prefix='/api/empresa')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)