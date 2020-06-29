import hashlib
from buzones.acuse import Acuse


class Mensaje(object):
    """ Mensaje recibido en el Buzón """

    def __init__(self, config, email, asunto, adjuntos):
        self.config = config
        self.email = email
        self.asunto = asunto
        self.adjuntos = adjuntos
        self.acuse = Acuse(self.config)
        self.ya_guardado = False
        self.ya_respondido = False

    def guardar_adjuntos(self, ruta):
        """ Clasificar los adjuntos en el mensaje """
        if self.ya_guardado is False:
            if len(self.adjuntos) > 0:
                for adjunto in self.adjuntos:
                    adjunto.establecer_ruta(ruta)
                    adjunto.guardar()
            self.ya_guardado = True

    def crear_identificador(self):
        """ Entrega el identificador del documento """
        adjuntos_archivos_lista = [adjunto.archivo for adjunto in self.adjuntos]
        cadena = self.email + '|' + '|'.join(adjuntos_archivos_lista)
        identificador = hashlib.sha256(self.config.salt.encode() + cadena.encode()).hexdigest()
        return(identificador)

    def enviar_acuse(self, destinatario):
        """ Enviar acuse vía correo electrónico """
        if self.ya_guardado is False:
            raise Exception('ERROR: No puede enviar acuse porque no ha guardado los adjuntos.')
        if self.ya_respondido is False:
            self.acuse.crear_asunto()
            self.acuse.crear_contenido(
                identificador=self.crear_identificador(),
                autoridad=destinatario['autoridad'],
                distrito=destinatario['distrito'],
                archivos=['archivos'],
            )
            self.acuse.enviar(self.email)
            self.ya_respondido = True

    def __repr__(self):
        if len(self.adjuntos) > 0:
            adjuntos_repr = '\n    '.join([repr(adjunto) for adjunto in self.adjuntos])
            if self.ya_respondido:
                return('<Mensaje> Respondido de {}\n    {}\n  {}'.format(self.email, adjuntos_repr, repr(self.acuse)))
            elif self.ya_guardado:
                return('<Mensaje> Guardado de {}\n    {}'.format(self.email, adjuntos_repr))
            elif len(self.adjuntos) > 0:
                return('<Mensaje> De {}\n    {}'.format(self.email, adjuntos_repr))
        else:
            return('<Mensaje> De {} SIN ADJUNTOS'.format(self.email))
