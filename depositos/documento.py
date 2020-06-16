import hashlib
import os
from depositos.acuse import Acuse


class Documento(object):
    """ Documento en el depósito """

    def __init__(self, config, ruta):
        self.config = config
        self.ruta = ruta
        self.directorio, self.archivo = os.path.split(ruta)
        if '/' in self.directorio:
            separados = self.directorio.split('/')
            self.distrito = separados[0]
            self.autoridad = separados[1]
        else:
            self.distrito = None
            self.autoridad = None
        self.acuse = None
        self.identificador = None

    def definir_identificador(self):
        cadena = f'{self.distrito}|{self.autoridad}|{self.archivo}'
        self.identificador = hashlib.sha256(self.config.salt.encode() + cadena.encode()).hexdigest()
        return(self.identificador)

    def definir_acuse(self):
        if self.identificador is None:
            self.definir_identificador()
        self.acuse = Acuse(self.config)
        self.acuse.elaborar_asunto()
        self.acuse.elaborar_contenido(
            identificador=self.identificador,
            distrito=self.distrito,
            autoridad=self.autoridad,
            archivos=[self.archivo],
        )
        return(self.acuse)

    def enviar_acuse(self, destinatario_email):
        self.acuse.enviar(destinatario_email)

    def __repr__(self):
        return('Documento')
