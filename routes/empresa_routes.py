from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
import oracledb

from config_app.connection import get_connection


empresa_bp = Blueprint('empresa', __name__)

@empresa_bp.route('/crear_y_asociar_empresa', methods=['POST'])
@jwt_required()
def crear_y_asociar_empresa():
    try:
        data = request.json
        nombre = data.get("nombre")
        nit = data.get("nit")
        direccion = data.get("direccion")
        logo = data.get("logo")  # Se espera que sea un string en base64
        correo_cliente = data.get("correo_cliente")
        usuario_modificacion = data.get("usuario_modificacion")

        if not all([nombre, nit, direccion, logo, correo_cliente, usuario_modificacion]):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Conexión a la base de datos
        conn = get_connection()
        
        if conn is None:
            return jsonify({"error": "No se pudo conectar con la base de datos"}), 500
        
        cursor = conn.cursor()

        # Declarar variable de salida para el procedimiento almacenado
        p_resultado = cursor.var(str)

        # Llamar al procedimiento almacenado
        cursor.callproc("crear_y_asociar_empresa", [
            nombre, 
            nit, 
            direccion, 
            logo, 
            correo_cliente, 
            usuario_modificacion, 
            p_resultado
        ])

        # Obtener el resultado
        resultado = p_resultado.getvalue()

        return jsonify({"mensaje": resultado}), 200

    except oracledb.DatabaseError as e:
        error, = e.args
        return jsonify({"error": f"Error de base de datos: {error.message}"}), 500

    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
