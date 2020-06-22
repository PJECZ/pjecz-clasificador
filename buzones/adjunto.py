class Adjunto(object):
    """ Archivo adjunto en un mensaje """

    def __init__(self, config, archivo_nombre, contenido_tipo, contenido_binario):
        self.config = config
        self.archivo_nombre = archivo_nombre
        self.contenido_tipo = contenido_tipo
        self.contenido_binario = contenido_binario

    def guardar_adjuntos(self):
        """ Guardar adjuntos en el depósito """
        # Determinar la ruta de destino a donde depositar los archivos adjuntos
        # Validar que exista el subdirectorio
        # Si no existen, se crean los subdirectorios del año y mes presente
        # Si es un archivo adjunto y termina con pdf
        pass

    def __repr__(self):
        return(f'<Adjunto> Tipo: {self.contenido_tipo} Nombre: {self.archivo_nombre}')
