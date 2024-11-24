from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import jwt_required
import oracledb
from config_app.connection import get_connection



dashboard_bp = Blueprint('dashboard', __name__)
@jwt_required()
@dashboard_bp.route('/cliente', methods=['POST'])

def dashboard_cliente():
    try:
        # Obtener el correo del cliente desde el cuerpo de la solicitud
        data = request.get_json()
        correo = data.get("correo")
        if not correo:
            return jsonify({"error": "El campo 'correo' es obligatorio"}), 400

        # Conectar a la base de datos
        conn = get_connection()
        cursor = conn.cursor()
        # Declarar la variable para el parámetro de salida (CLOB)
        resultado_clob = cursor.var(oracledb.CLOB)

        


        # Llamar al procedimiento almacenado
        cursor.callproc("DASHBOARD_CLIENTE_SP", [correo, resultado_clob])

        # Obtener el contenido del CLOB como texto
        resultado_json = resultado_clob.getvalue()

        resultado_texto = str(resultado_json) if resultado_json else "{}"  # Asegurarnos de que sea cadena
            # Convertir el string en un objeto JSON
        json_data = json.loads(resultado_texto)

      
        # Convertir el resultado a un diccionario y devolver como respuesta JSON
        return jsonify({"resultado": json_data}), 200

    except oracledb.Error as e:
        error, = e.args
        return jsonify({"error": f"Error de base de datos: {error.message}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500