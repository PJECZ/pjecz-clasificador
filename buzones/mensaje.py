"""
Mensaje
"""
import logging
import hashlib
from buzones.acuse import Acuse


bitacora = logging.getLogger(__name__)
bitacora.setLevel(logging.INFO)
formato = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
empunadura = logging.FileHandler('buzones.log')
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)


class Mensaje(object):
    """ Mensaje recibido en el Buzón """

    def __init__(self, config, email, asunto, adjuntos):
        self.config = config
        self.email = email
        self.asunto = asunto
        self.adjuntos = adjuntos
        self.adjuntos_descartados = []
        self.acuse = Acuse(self.config)
        self.ya_guardado = False
        self.ya_guardado_adjuntos_validos = False
        self.ya_respondido = False

    def guardar_adjuntos(self, cliente_ruta):
        """ Guardar los adjuntos en el mensaje, entrega verdadero si guarda adjuntos válidos """
        if self.ya_guardado is False:
            if len(self.adjuntos) > 0:
                adjuntos_validos = []
                for adjunto in self.adjuntos:
                    adjunto.establecer_ruta(cliente_ruta)
                    if adjunto.guardar():
                        adjuntos_validos.append(adjunto)
                    else:
                        self.adjuntos_descartados.append(adjunto)
                self.adjuntos = adjuntos_validos
                if len(self.adjuntos) > 0:
                    self.ya_guardado_adjuntos_validos = True
                else:
                    bitacora.warning('[%s] No son válidos los adjuntos del mensaje de %s', self.config.rama, self.email)
            else:
                bitacora.warning('[%s] Sin adjuntos el mensaje de %s', self.config.rama, self.email)
            self.ya_guardado = True
            return self.ya_guardado_adjuntos_validos

    def crear_identificador(self):
        """ Entrega el identificador del documento """
        adjuntos_archivos_lista = [adjunto.archivo for adjunto in self.adjuntos]
        cadena = self.email + '|' + '|'.join(adjuntos_archivos_lista)
        identificador = hashlib.sha256(self.config.salt.encode() + cadena.encode()).hexdigest()
        return identificador

    def enviar_acuse(self, destinatario):
        """ Enviar acuse vía correo electrónico, entrega verdadero si lo hace """
        if self.ya_guardado is False:
            raise Exception('ERROR: No puede enviar acuse porque no ha guardado los adjuntos.')
        if self.ya_guardado_adjuntos_validos is False:
            return False
        if self.ya_respondido:
            return False
        if len(self.adjuntos) == 0:
            bitacora.warning('[%s] No tiene adjuntos el mensaje de %s', self.config.rama, self.email)
            return False
        self.acuse.crear_asunto()
        self.acuse.crear_contenido(
            identificador=self.crear_identificador(),
            autoridad=destinatario['autoridad'],
            distrito=destinatario['distrito'],
            archivos=[adjunto.archivo for adjunto in self.adjuntos],
        )
        self.acuse.enviar(self.email)
        self.ya_respondido = True
        adjuntos_texto = ', '.join([adjunto.archivo for adjunto in self.adjuntos])
        bitacora.info('[%s] Acuse enviado a %s por %s', self.config.rama, self.email, adjuntos_texto)
        return True

    def __repr__(self):
        if len(self.adjuntos) > 0:
            adjuntos_repr = '\n    '.join([repr(adjunto) for adjunto in self.adjuntos])
            if self.ya_respondido:
                return '<Mensaje> Respondido de {}\n    {}\n    {}'.format(self.email, adjuntos_repr, repr(self.acuse))
            elif self.ya_guardado:
                return '<Mensaje> Guardado de {}\n    {}'.format(self.email, adjuntos_repr)
            elif len(self.adjuntos) > 0:
                return '<Mensaje> De {}\n    {}'.format(self.email, adjuntos_repr)
        return '<Mensaje> De {} SIN ADJUNTOS'.format(self.email)
