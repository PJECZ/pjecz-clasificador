import os
from depositos.acuse import Acuse


class Documento(object):
    """ Documento en el depósito """

    def __init__(self, config, ruta):
        self.config = config
        self.ruta = ruta
        self.archivo = os.path.basename(ruta)

    def enviar_acuse(self, destinatario_email):
        acuse = Acuse(self.config)
        acuse.elaborar_asunto()
        acuse.elaborar_contenido(
            identificador='123123',
            autoridad='autoridad',
            distrito='distrito',
            archivos=self.archivo,
        )
        acuse.enviar(destinatario_email)

    def __repr__(self):
        return('Documento')
