from flask import Blueprint, request, jsonify
import bcrypt
from oracledb import connect
from config_app.connection import get_connection

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/registro', methods=['POST'])
def registro_usuario():
    data = request.json
    nombre = data['nombre']
    apellido = data['apellido']
    email = data['email']
    password = data['password']

    # Generar la contraseña hasheada
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        # Conectar a la base de datos y llamar al procedimiento almacenado
        conn = get_connection()
        cursor = conn.cursor()
        resultado = cursor.var(str)
        
        # Llamar al procedimiento almacenado
        cursor.callproc('CREAR_CLIENTE_SP', [email,nombre,apellido,hashed_password,resultado])
        mensaje = resultado.getvalue()
        conn.commit()

        return jsonify({"message": mensaje})
    except Exception as e:
        # Si ocurre un error, devolver mensaje de error
        return jsonify({"error": str(e)}), 400