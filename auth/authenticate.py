from models.cliente import Cliente

def authenticate(cursor, correo, contraseña_ingresada):
    try:
        # Crear variables para recibir los valores de salida del procedimiento almacenado
        mensaje = cursor.var(str)     # Variable de salida para el mensaje
        resultado = cursor.var(int)   # Variable de salida para el resultado (1 para éxito, 0 para error)

        # Llamar al procedimiento almacenado para validar login
        cursor.callproc("LOGIN_CLIENTE_SP", [
            correo,                 # Parámetro de entrada: correo
            contraseña_ingresada,   # Parámetro de entrada: contraseña
            mensaje,                # Parámetro de salida: mensaje
            resultado               # Parámetro de salida: resultado
        ])
        
        # Obtener los valores de las variables de salida
        mensaje_valor = mensaje.getvalue()
        resultado_valor = resultado.getvalue()

        # Verificar el resultado del procedimiento almacenado
        if resultado_valor == 1:
            # Consulta los datos del cliente si el login fue exitoso
            cursor.execute("""
                SELECT 
                    correo, 
                    nombre, 
                    apellido, 
                    activo, 
                    fecha_creacion, 
                    ultimo_inicio_sesion
                FROM CLIENTE
                WHERE correo = :correo
            """, correo=correo)
            
            cliente_data = cursor.fetchone()
            
            if not cliente_data:
                return None
            
            # Crear instancia de cliente
            cliente = Cliente(
                correo=cliente_data[0],
                nombre=cliente_data[1],
                apellido=cliente_data[2],
                activo=cliente_data[3],
                fecha_creacion=cliente_data[4],
                ultimo_inicio_sesion=cliente_data[5]
            )
            
            cursor.connection.commit()
            
            return cliente
        else:
            # Si el resultado es 0, devolver el mensaje de error
            return mensaje_valor
    
    except Exception as e:
        print(f"Error en autenticación: {e}")
        cursor.connection.rollback()
        raise e
