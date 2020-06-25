from imap_tools import MailBox, Q
from buzones.mensaje import Mensaje
from buzones.adjunto import Adjunto


class Buzon(object):
    """ Buzon """

    def __init__(self, config):
        self.config = config
        self.mensajes = []
        self.mensajes_descartados = []
        self.ya_leidos = False
        self.ya_clasificados = False

    def leer_mensajes(self):
        """ Leer los mensajes en el buzón, entrega listado de Mensajes """
        if self.ya_leidos:
            return(self.mensajes)
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
        return(self.mensajes)

    def guardar_adjuntos(self, remitentes):
        """ Guardar los adjuntos en los mensajes """
        if self.ya_clasificados is True:
            return(self.mensajes)
        mensajes_clasificados = []
        for mensaje in self.mensajes:
            if mensaje.email in remitentes:
                remitente = remitentes[mensaje.email]
                mensaje.guardar_adjuntos(remitente['ruta'])
                mensajes_clasificados.append(mensaje)
            else:
                self.mensajes_descartados.append(mensaje)
        self.mensajes = mensajes_clasificados
        self.ya_clasificados = True
        return(self.mensajes)

    def responder_con_acuses(self):
        """ Responder con acuses los mensajes """
        for mensaje in self.mensajes:
            if mensaje.ya_respondido is False:
                mensaje.enviar_acuse()

    def __repr__(self):
        if self.ya_clasificados:
            mensajes_repr = [repr(mensaje) for mensaje in self.mensajes]
            return('<Buzon> Clasificados {}, descartados {}\n  {}'.format(
                len(self.mensajes),
                len(self.mensajes_descartados),
                '\n  '.join(mensajes_repr),
            ))
        elif self.ya_leidos:
            mensajes_repr = [repr(mensaje) for mensaje in self.mensajes]
            return('<Buzon> Leídos {}\n  {}'.format(len(self.mensajes), '\n  '.join(mensajes_repr)))
        else:
            return('<Buzon>')
