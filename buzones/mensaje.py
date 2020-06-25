from buzones.acuse import Acuse


class Mensaje(object):
    """ Mensaje recibido en el Buzón """

    def __init__(self, config, email, asunto, adjuntos):
        self.config = config
        self.email = email
        self.asunto = asunto
        self.adjuntos = adjuntos
        self.ya_respondido = False
        self.ya_guardado = False

    def guardar_adjuntos(self, ruta):
        """ Clasificar los adjuntos en el mensaje """
        if len(self.adjuntos) == 0:
            return([])
        rutas = []
        for adjunto in self.adjuntos:
            rutas.append(adjunto.establecer_ruta(ruta))
            adjunto.guardar()
        return(rutas)

    def enviar_acuse(self):
        """ Enviar acuse vía correo electrónico """
        if self.ya_respondido is False:
            acuse = Acuse(self.config)
            acuse.crear_asunto()
            acuse.crear_contenido('id', 'autoridad', 'distrito', ['archivos'])
            acuse.enviar(self.email)
            self.ya_respondido = True

    def __repr__(self):
        if len(self.adjuntos) > 0:
            adjuntos_repr = [repr(adjunto) for adjunto in self.adjuntos]
            return('<Mensaje> De: {}\n    {}'.format(self.email, '\n    '.join(adjuntos_repr)))
        else:
            return('<Mensaje> De: {}, Asunto: {}, SIN ADJUNTOS.'.format(self.email, self.asunto))
