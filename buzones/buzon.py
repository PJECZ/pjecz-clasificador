import logging
from imap_tools import MailBox, Q
from buzones.mensaje import Mensaje
from buzones.adjunto import Adjunto


bitacora = logging.getLogger(__name__)
bitacora.setLevel(logging.INFO)
formato = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
empunadura = logging.FileHandler('buzones.log')
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)


class Buzon(object):
    """ Buzon """

    def __init__(self, config):
        self.config = config
        self.mensajes = []
        self.mensajes_descartados = []
        self.ya_leidos = False
        self.ya_guardados = False
        self.ya_respondidos = False

    def leer_mensajes(self):
        """ Leer los mensajes en el buzón, entrega listado de Mensajes """
        if self.ya_leidos is False:
            with MailBox(self.config.servidor_imap).login(self.config.email_direccion, self.config.email_contrasena) as mailbox:
                for msg in mailbox.fetch(Q(seen=False)):
                    adjuntos = []
                    for adj in msg.attachments:
                        adjuntos.append(Adjunto(
                            config=self.config,
                            archivo=adj.filename,
                            contenido_tipo=adj.content_type,
                            contenido_binario=adj.payload,
                        ))
                    self.mensajes.append(Mensaje(
                        config=self.config,
                        email=msg.from_,
                        asunto=msg.subject,
                        adjuntos=adjuntos,
                    ))
            self.ya_leidos = True
            bitacora.info('[{}] Leídos {} mensajes'.format(self.config.rama, len(self.mensajes)))
        return(self.mensajes)

    def guardar_adjuntos(self, remitentes):
        """ Guardar los adjuntos en los mensajes, entrega listado de Mensajes """
        if self.ya_leidos is False:
            self.leer_mensajes()
        if self.ya_guardados is False:
            mensajes_clasificados = []
            for mensaje in self.mensajes:
                if mensaje.email in remitentes:
                    bitacora.info('[{}] Mensaje reconocido de {}'.format(self.config.rama, mensaje.email))
                    remitente = remitentes[mensaje.email]
                    if mensaje.guardar_adjuntos(remitente['ruta']):
                        mensajes_clasificados.append(mensaje)
                    else:
                        self.mensajes_descartados.append(mensaje)
                else:
                    bitacora.warning('[{}] Mensaje descartado de {}'.format(self.config.rama, mensaje.email))
                    self.mensajes_descartados.append(mensaje)
            self.mensajes = mensajes_clasificados
            self.ya_guardados = True
        return(self.mensajes)

    def responder_con_acuses(self, remitentes):
        """ Responder con acuses """
        if self.ya_leidos is False:
            raise Exception('ERROR: No puede responder con acuses porque no ha leído los mensajes.')
        if self.ya_guardados is False:
            raise Exception('ERROR: No puede responder con acuses porque no ha guardado los adjuntos.')
        if self.ya_respondidos is False:
            contador = 0
            for mensaje in self.mensajes:
                if mensaje.ya_respondido is False and mensaje.email in remitentes:
                    mensaje.enviar_acuse(remitentes[mensaje.email])
                    contador += 1
            bitacora.info('[{}] Respondidos {} mensajes'.format(self.config.rama, contador))
            self.ya_respondidos = True

    def __repr__(self):
        if len(self.mensajes) > 0:
            mensajes_repr = '\n  '.join([repr(mensaje) for mensaje in self.mensajes])
            if self.ya_respondidos:
                return('<Buzon> Respondidos {}, descartados {}\n  {}'.format(len(self.mensajes), len(self.mensajes_descartados), mensajes_repr))
            elif self.ya_guardados:
                return('<Buzon> Guardados {}, descartados {}\n  {}'.format(len(self.mensajes), len(self.mensajes_descartados), mensajes_repr))
            elif self.ya_leidos:
                return('<Buzon> Leídos {}\n  {}'.format(len(self.mensajes), mensajes_repr))
            else:
                return('<Buzon>')
        else:
            return('<Buzon> SIN MENSAJES')
