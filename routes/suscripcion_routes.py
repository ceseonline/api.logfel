from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
import oracledb

from config_app.connection import get_connection

suscripcion_bp = Blueprint('suscripcion', __name__)

@suscripcion_bp.route('/validar_suscripcion', methods=['POST'])
@jwt_required()
def validar_suscripcion():
    data = request.get_json()
    correo = data.get('correo', None)
    
    if not correo:
        return jsonify({"error": "El correo es obligatorio"}), 400
    
    try:
        conn = get_connection()
        if conn is None:
            return jsonify({"error": "No se pudo conectar con la base de datos"}), 500
        
        cursor = conn.cursor()
        result = cursor.var(str)
        cursor.callproc("VALIDAR_SUSCRIPCION_SP", [correo, result])

        cursor.close()
        conn.close()

        return jsonify({"status": result.getvalue()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@suscripcion_bp.route('/crear_suscripcion', methods=['POST'])
@jwt_required()
def crear_suscripcion():
    try:
        conn = get_connection()

        data = request.get_json()
        correo = data.get("correo")
        id_tipo_suscripcion = data.get("id_tipo_suscripcion")
        
        if not correo:
            return jsonify({"error": "El correo es obligatorio"}), 400
        
        cursor = conn.cursor()
        result = cursor.var(str)

        cursor.callproc(
            "CREAR_SUSCRIPCION_SP",
            [
                correo,
                id_tipo_suscripcion,
                result
            ]
        )
        return jsonify({"mensaje":result.getvalue()})  # El mensaje de salida está en la posición 3   
    except oracledb.DatabaseError as e:
        error, = e.args
        if error.code == 20002:
            return jsonify({'error': error.message}), 400
        else:
            return jsonify({'error': f'Error: {error.message}'}), 500
    finally:
        cursor.close()
        conn.close()

@suscripcion_bp.route('/obtener_planes', methods=['GET'])
@jwt_required()
def obtener_planes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_TIPO_SUSCRIPCION, DESCRIPCION, PRECIO FROM TIPO_SUSCRIPCION")
        planes = cursor.fetchall()
        planes_data = []
        for plan in planes:
            planes_data.append({
                'id': plan[0],
                'descripcion': plan[1],
                'precio': plan[2],
            })
        return jsonify(planes_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500