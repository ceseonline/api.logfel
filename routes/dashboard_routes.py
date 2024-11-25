from flask import Blueprint, json, request, jsonify
from flask_jwt_extended import jwt_required
import oracledb
from config_app.connection import get_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/cliente', methods=['POST'])
@jwt_required()
def dashboard_cliente():
    try:
        data = request.get_json()
        correo = data.get("correo")
        if not correo:
            return jsonify({"error": "El campo 'correo' es obligatorio"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        resultado_clob = cursor.var(oracledb.CLOB)
        cursor.callproc("DASHBOARD_CLIENTE_SP", [correo, resultado_clob])
        resultado_json = resultado_clob.getvalue()
        resultado_texto = str(resultado_json) if resultado_json else "{}"  # Asegurarnos de que sea cadena
        json_data = json.loads(resultado_texto)
      
        return jsonify({"resultado": json_data}), 200
    except oracledb.Error as e:
        error, = e.args
        return jsonify({"error": f"Error de base de datos: {error.message}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500