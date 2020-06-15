from imap_tools import MailBox
from buzones.mensaje import Mensaje


class Buzon(object):
    """ Buzon """

    def __init__(self, config):
        self.config = config
        self.mensajes = []

    def leer_mensajes(self):
        """ Leer mensajes """
        self.mensajes = []
        with MailBox(self.config.servidor_imap).login(self.config.email_direccion, self.config.email_contrasena) as mailbox:
            for msg in mailbox.fetch():
                mensaje = Mensaje(
                    config=self.config,
                    email='',
                    asunto=msg.subject,
                    adjuntos=[],
                )
                self.mensajes.append(mensaje)
        return(self.mensajes)

    def clasificar_mensajes(self):
        """ Clasificar mensajes """
        pass

    def responder_mensajes(self):
        """ Responder mensajes """
        pass

    def __repr__(self):
        return('<Buzon>')
