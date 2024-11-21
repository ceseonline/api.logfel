import bcrypt
from flask import Blueprint,request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required, set_access_cookies, unset_jwt_cookies
from config_app.connection import get_connection
from auth.authenticate import authenticate


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
   

    data = request.get_json()
    correo = data.get('email')
    contraseña = data.get('password')
    if not correo or not contraseña:
        return jsonify({'error': 'Se requieren correo y contraseña'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cliente_auth = authenticate(cursor, correo, contraseña)
        if cliente_auth == "inactive":
            return jsonify({'error': 'Usuario inactivo. Contacte al administrador'}), 401
        elif cliente_auth:
            access_token = create_access_token(identity=cliente_auth.correo)
        
            response = make_response(jsonify({
                'message': 'Login exitoso',
                'user': cliente_auth.to_dict()
            }))   
            # Configurar la cookie con el token
            set_access_cookies(response, access_token)
            
            return response
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
       
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@auth_bp.route('/check-token', methods=['GET'])
@jwt_required()
def check_token():
    try:
        # Intentamos obtener la identidad del JWT
        current_user = get_jwt_identity()
        return jsonify({'authenticated': True, 'user': current_user}), 200
    except Exception as e:
        return jsonify({'authenticated': False}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    print(f"JWT Claims: {get_jwt()}")
    response = make_response(jsonify({"msg": "Logout exitoso"}), 200)
    unset_jwt_cookies(response)
    return response