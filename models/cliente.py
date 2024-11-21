class Cliente:
    
    def __init__(self,correo, nombre, apellido, activo, fecha_creacion, ultimo_inicio_sesion):
        self.correo = correo
        self.nombre = nombre
        self.apellido = apellido
        self.activo = activo
        self.fecha_creacion = fecha_creacion
        self.ultimo_inicio_sesion = ultimo_inicio_sesion

    def to_dict(self):
        return {
            'correo': self.correo,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'ultimo_inicio_sesion': self.ultimo_inicio_sesion.isoformat() if self.ultimo_inicio_sesion else None
        }