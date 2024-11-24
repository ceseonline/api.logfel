from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from config_app.connection import get_connection

suscripcion_bp = Blueprint('suscripcion', __name__)

@jwt_required()

@suscripcion_bp.route('/validar_suscripcion', methods=['POST'])
def validar_suscripcion():
    # Obtenemos el correo del cuerpo de la solicitud
    data = request.get_json()
    correo = data.get('correo', None)
    
    if not correo:
        return jsonify({"error": "El correo es obligatorio"}), 400
    
    # Llamamos al procedimiento almacenado para validar la suscripción
    try:
        conn = get_connection()
        
        if conn is None:
            return jsonify({"error": "No se pudo conectar con la base de datos"}), 500
        
        cursor = conn.cursor()

        # Definir el tipo de salida que recibe el procedimiento almacenado
        result = cursor.var(str)

        # Llamamos al SP
        cursor.callproc("VALIDAR_SUSCRIPCION_SP", [correo, result])

        # Cerramos el cursor y la conexión
        cursor.close()
        conn.close()

        # Devolvemos el resultado al frontend
        return jsonify({"status": result.getvalue()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
