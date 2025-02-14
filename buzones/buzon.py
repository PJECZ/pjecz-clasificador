"""
Buzones, Buzon
"""
import logging
from imap_tools import MailBox, AND

from buzones.mensaje import Mensaje
from buzones.adjunto import Adjunto

bitacora = logging.getLogger(__name__)
bitacora.setLevel(logging.INFO)
formato = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
empunadura = logging.FileHandler("buzones.log")
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)


class Buzon:
    """Buzon"""

    def __init__(self, config):
        """Inicializar"""
        self.config = config
        self.mensajes = []
        self.mensajes_descartados = []
        self.mensajes_desconocidos = []
        self.ya_leidos = False
        self.ya_guardados = False
        self.ya_respondidos_con_acuses = False
        self.ya_respondidos_con_rechazos = False

    def leer_mensajes(self):
        """Leer los mensajes en el buzón"""
        if self.ya_leidos is False:
            with MailBox(self.config.servidor_imap).login(self.config.email_direccion, self.config.email_contrasena) as mailbox:
                for msg in mailbox.fetch(AND(seen=False)):
                    adjuntos = []
                    for adj in msg.attachments:
                        adjuntos.append(
                            Adjunto(
                                config=self.config,
                                archivo=adj.filename,
                                contenido_tipo=adj.content_type,
                                contenido_binario=adj.payload,
                            )
                        )
                    self.mensajes.append(
                        Mensaje(
                            config=self.config,
                            email=msg.from_,
                            asunto=msg.subject,
                            adjuntos=adjuntos,
                        )
                    )
            self.ya_leidos = True
            bitacora.info("[%s] Leídos %s mensajes", self.config.rama, len(self.mensajes))

    def guardar_adjuntos(self, remitentes):
        """Guardar los adjuntos en los mensajes"""
        if self.ya_leidos is False:
            self.leer_mensajes()
        if self.ya_guardados is False:
            mensajes_clasificados = []
            for mensaje in self.mensajes:
                if str(mensaje.email).lower() in remitentes:
                    bitacora.info("[%s] Mensaje reconocido de %s", self.config.rama, mensaje.email)
                    remitente = remitentes[str(mensaje.email).lower()]
                    mensaje.guardar_adjuntos(remitente["ruta"])
                    if mensaje.hay_adjuntos_validos:
                        mensajes_clasificados.append(mensaje)
                    if mensaje.hay_adjuntos_rechazados:
                        self.mensajes_descartados.append(mensaje)
                else:
                    bitacora.warning("[%s] Mensaje descartado de %s", self.config.rama, mensaje.email)
                    self.mensajes_desconocidos.append(mensaje)
            self.mensajes = mensajes_clasificados
            self.ya_guardados = True

    def responder_con_acuses(self, remitentes):
        """Responder con acuses"""
        if self.ya_leidos is False:
            raise Exception("ERROR: No puede responder con acuses porque no ha leído los mensajes.")
        if self.ya_guardados is False:
            raise Exception("ERROR: No puede responder con acuses porque no ha guardado los adjuntos.")
        if self.ya_respondidos_con_acuses is False and len(self.mensajes) > 0:
            contador = 0
            for mensaje in self.mensajes:
                if mensaje.ya_enviados_acuses is False and str(mensaje.email).lower() in remitentes:
                    mensaje.enviar_acuse(remitentes[str(mensaje.email).lower()])
                    contador += 1
            if contador > 0:
                bitacora.info("[%s] Respondidos %s mensajes con acuses", self.config.rama, contador)
            self.ya_respondidos_con_acuses = True

    def responder_con_rechazos(self, remitentes):
        """Responder con rechazos"""
        if self.ya_leidos is False:
            raise Exception("ERROR: No puede responder con rechazos porque no ha leído los mensajes.")
        if self.ya_guardados is False:
            raise Exception("ERROR: No puede responder con rechazos porque no ha guardado los adjuntos.")
        if self.ya_respondidos_con_rechazos is False and len(self.mensajes_descartados) > 0:
            contador = 0
            for mensaje in self.mensajes_descartados:
                if mensaje.ya_enviados_rechazos is False and str(mensaje.email).lower() in remitentes:
                    mensaje.enviar_rechazo(remitentes[str(mensaje.email).lower()])
                    contador += 1
            if contador > 0:
                bitacora.info("[%s] Respondidos %s mensajes con rechazos", self.config.rama, contador)
            self.ya_respondidos_con_rechazos = True

    def __repr__(self):
        """Representación"""
        if len(self.mensajes) > 0:
            mensajes_repr = "\n  ".join([repr(mensaje) for mensaje in self.mensajes])
            if self.ya_respondidos_con_acuses or self.ya_respondidos_con_rechazos:
                return "<Buzon> Respondidos acuses {}, rechazados {}\n  {}".format(len(self.mensajes), len(self.mensajes_descartados), mensajes_repr)
            elif self.ya_guardados:
                return "<Buzon> Guardados {}, rechazados {}\n  {}".format(len(self.mensajes), len(self.mensajes_descartados), mensajes_repr)
            elif self.ya_leidos:
                return "<Buzon> Leídos {}\n  {}".format(len(self.mensajes), mensajes_repr)
            else:
                return "<Buzon>"
        return "<Buzon> SIN MENSAJES"
