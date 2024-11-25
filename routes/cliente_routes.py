from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
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
    try:
        conn = get_connection()
        cursor = conn.cursor()
        resultado = cursor.var(str)
        cursor.callproc('CREAR_CLIENTE_SP', [email,nombre,apellido,password,resultado])
        mensaje = resultado.getvalue()
        conn.commit()
        return jsonify({"message": mensaje})
    except Exception as e:
        return jsonify({"error": str(e)}), 400