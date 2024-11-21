from datetime import timedelta
from flask_jwt_extended import JWTManager
from config_app.connection import get_connection


def get_jwt_secret():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT secret_key FROM app_config WHERE config_name = 'JWT_SECRET_KEY'")
        result = cursor.fetchone()
        print("result JWT" , result[0])
        return str(result[0]).strip()
        #if result else os.getenv('JWT_SECRET_KEY', 'default-secret-key')
    except Exception as e:
        print(f"Error getting JWT secret: {e}")
        return "ERROR" 
        #os.getenv('JWT_SECRET_KEY', 'default-secret-key')
    finally:
        cursor.close()

def configure_jwt(app):
  
    app.config['JWT_SECRET_KEY'] = get_jwt_secret()
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = True  # Para HTTPS
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    app.config['JWT_COOKIE_SAMESITE'] = 'Strict'
    return JWTManager(app)