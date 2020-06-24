from imap_tools import MailBox, Q
from buzones.mensaje import Mensaje
from buzones.adjunto import Adjunto


class Buzon(object):
    """ Buzon """

    def __init__(self, config):
        self.config = config
        self.mensajes = []

    def leer_mensajes(self):
        """ Leer los mensajes en el buzón, entrega listado de Mensajes """
        self.mensajes = []
        with MailBox(self.config.servidor_imap).login(self.config.email_direccion, self.config.email_contrasena) as mailbox:
            for msg in mailbox.fetch(Q(seen=False)):
                adjuntos = []
                for adj in msg.attachments:
                    adjuntos.append(Adjunto(
                        config=self.config,
                        archivo_nombre=adj.filename,
                        contenido_tipo=adj.content_type,
                        contenido_binario=adj.payload,
                    ))
                self.mensajes.append(Mensaje(
                    config=self.config,
                    email=msg.from_,
                    asunto=msg.subject,
                    adjuntos=adjuntos,
                ))
        return(self.mensajes)

    def clasificar_mensajes(self):
        """ Clasificar mensajes """
        if len(self.mensajes) == 0:
            raise Exception('AVISO: Sin mensajes.')
        for mensaje in self.mensajes:
            mensaje.clasificar_adjuntos()

    def responder_mensajes(self):
        """ Responder mensajes """
        pass

    def __repr__(self):
        if len(self.mensajes) > 0:
            return('<Buzon> {} mensajes'.format(len(self.mensajes)))
        else:
            return('<Buzon> NO HAY mensajes sin leer.')
