"""
Buzones, Mensaje
"""
import logging
import hashlib
from buzones.acuse import Acuse
from buzones.rechazo import Rechazo
from buzones.adjunto import AdjuntoRechazo

bitacora = logging.getLogger(__name__)
bitacora.setLevel(logging.INFO)
formato = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
empunadura = logging.FileHandler("buzones.log")
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)


class Mensaje:
    """Mensaje recibido en el Buzón"""

    def __init__(self, config, email, asunto, adjuntos):
        """Inicializar"""
        self.config = config
        self.email = email
        self.asunto = asunto
        self.adjuntos = adjuntos
        self.adjuntos_rechazados = []
        self.acuse = Acuse(self.config)
        self.rechazo = Rechazo(self.config)
        self.ya_guardado = False
        self.hay_adjuntos_validos = False
        self.hay_adjuntos_rechazados = False
        self.ya_enviados_acuses = False
        self.ya_enviados_rechazos = False

    def guardar_adjuntos(self, cliente_ruta):
        """Guardar los adjuntos en el mensaje"""
        if self.ya_guardado is False:
            if len(self.adjuntos) > 0:
                adjuntos_validos = []
                for adjunto in self.adjuntos:
                    adjunto.establecer_ruta(cliente_ruta)
                    try:
                        adjunto.guardar()
                        adjuntos_validos.append(adjunto)
                    except AdjuntoRechazo:
                        self.adjuntos_rechazados.append(adjunto)
                self.adjuntos = adjuntos_validos
                self.hay_adjuntos_validos = len(self.adjuntos) > 0
                self.hay_adjuntos_rechazados = len(self.adjuntos_rechazados) > 0
            else:
                bitacora.warning("[%s] Sin adjuntos el mensaje de %s", self.config.rama, self.email)
            self.ya_guardado = True

    def crear_identificador(self):
        """Entrega el identificador del documento"""
        adjuntos_archivos_lista = [adjunto.archivo for adjunto in self.adjuntos]
        cadena = self.email + "|" + "|".join(adjuntos_archivos_lista)
        identificador = hashlib.sha256(self.config.salt.encode() + cadena.encode()).hexdigest()
        return identificador

    def enviar_acuse(self, destinatario):
        """Enviar acuse vía correo electrónico"""
        if self.ya_guardado is False:
            raise Exception("ERROR: No puede enviar acuse porque no ha guardado los adjuntos.")
        if self.ya_enviados_acuses:
            return False
        self.ya_enviados_acuses = True
        if self.hay_adjuntos_validos is False:
            return False
        self.acuse.crear_asunto()
        self.acuse.crear_contenido(
            identificador=self.crear_identificador(),
            autoridad=destinatario["autoridad"],
            distrito=destinatario["distrito"],
            archivos=[adjunto.archivo for adjunto in self.adjuntos],
        )
        self.acuse.enviar(self.email)
        bitacora.info("[%s] Acuse enviado a %s por %s", self.config.rama, self.email, ", ".join([adjunto.archivo for adjunto in self.adjuntos]))

    def enviar_rechazo(self, destinatario):
        """Enviar rechazo vía correo electrónico"""
        if self.ya_guardado is False:
            raise Exception("ERROR: No puede enviar rechazos porque no ha guardado los adjuntos.")
        if self.ya_enviados_rechazos:
            return False
        self.ya_enviados_rechazos = True
        if self.hay_adjuntos_rechazados is False:
            return False
        self.rechazo.crear_asunto()
        self.rechazo.crear_contenido(
            causas=[adjunto.rechazo_mensaje for adjunto in self.adjuntos_rechazados],
            autoridad=destinatario["autoridad"],
            distrito=destinatario["distrito"],
            archivos=[adjunto.archivo for adjunto in self.adjuntos_rechazados],
        )
        self.rechazo.enviar(self.email)
        bitacora.info("[%s] Rechazo enviado a %s por %s", self.config.rama, self.email, ", ".join([adjunto.archivo for adjunto in self.adjuntos_rechazados]))

    def __repr__(self):
        """Representación"""
        if self.ya_guardado:
            if self.ya_enviados_acuses and self.hay_adjuntos_validos and self.ya_enviados_rechazos and self.hay_adjuntos_rechazados:
                adjuntos_validos_repr = "\n    ".join([repr(adjunto) for adjunto in self.adjuntos])
                adjuntos_rechazados_repr = "\n    ".join([repr(adjunto) for adjunto in self.adjuntos_rechazados])
                return "<Mensaje> De {} con acuses y rechazos\n    {}\n    {}".format(self.email, adjuntos_validos_repr, adjuntos_rechazados_repr)
            elif self.ya_enviados_acuses and self.hay_adjuntos_validos:
                adjuntos_validos_repr = "\n    ".join([repr(adjunto) for adjunto in self.adjuntos])
                return "<Mensaje> De {} con acuses\n    {}".format(self.email, adjuntos_validos_repr)
            elif self.ya_enviados_rechazos and self.hay_adjuntos_rechazados:
                adjuntos_rechazados_repr = "\n    ".join([repr(adjunto) for adjunto in self.adjuntos_rechazados])
                return "<Mensaje> De {} con rechazos\n    {}".format(self.email, adjuntos_rechazados_repr)
            else:
                return "<Mensaje> De {} guardado".format(self.email)
        elif len(self.adjuntos) > 0:
            adjuntos_repr = "\n    ".join([repr(adjunto) for adjunto in self.adjuntos])
            return "<Mensaje> De {}\n    {}".format(self.email, adjuntos_repr)
        return "<Mensaje> De {} SIN ADJUNTOS".format(self.email)
