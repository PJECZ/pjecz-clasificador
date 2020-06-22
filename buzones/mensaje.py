class Mensaje(object):
    """ Mensaje recibido en el Buzón """

    def __init__(self, config, email, asunto, adjuntos):
        self.config = config
        self.email = email
        self.asunto = asunto
        self.adjuntos = adjuntos

    def clasificar_adjuntos(self):
        """ Clasificar los adjuntos en el depósito """
        if len(self.adjuntos) == 0:
            return('AVISO: Este mensaje no tiene archivos adjuntos.')
        return('Se clasificaron N archivos adjuntos.')

    def responder_con_acuse(self):
        """ Responder con acuse de recibido """
        pass

    def __repr__(self):
        if len(self.adjuntos) > 0:
            archivos_nombres = [adj.archivo_nombre for adj in self.adjuntos]
            return('<Mensaje> De: {}, Asunto: {}, Adjuntos: {}'.format(self.email, self.asunto, ','.join(archivos_nombres)))
        else:
            return('<Mensaje> De: {}, Asunto: {}, SIN ADJUNTOS.'.format(self.email, self.asunto))
