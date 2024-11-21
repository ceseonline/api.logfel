from models.cliente import Cliente

def authenticate(cursor, correo, contraseña):
        try:
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
                AND contraseña = :contraseña
            """, correo=correo, contraseña=contraseña)
            
            Cliente_data = cursor.fetchone()
            
            if not Cliente_data:
                return None
            
            # Crear instancia de usuario
            cliente = Cliente(
                correo=Cliente_data[0],
                nombre=Cliente_data[1],
                apellido=Cliente_data[2],
                activo=Cliente_data[3],
                fecha_creacion=Cliente_data[4],
                ultimo_inicio_sesion=Cliente_data[5]
            )
           
            # Verificar si el usuario está activo
            if not bool(cliente.activo):
                return "inactive"
                
            # Actualizar último inicio de sesión
            cursor.execute("""
                UPDATE Cliente 
                SET ultimo_inicio_sesion = CURRENT_TIMESTAMP 
                WHERE correo = :correo_cliente
            """, correo_cliente=cliente.correo)
            
            cursor.connection.commit()
            
            return cliente
            
        except Exception as e:
            print(f"Error en autenticación: {e}")
            cursor.connection.rollback()
            raise e
