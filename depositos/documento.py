import hashlib
import os
from depositos.acuse import Acuse


class Documento(object):
    """ Documento en el depósito """

    def __init__(self, config):
        self.config = config
        self.ruta = None
        self.directorio = None
        self.archivo = None
        self.distrito = None
        self.autoridad = None
        self.identificador = None
        self.acuse = None

    def establecer_ruta(self, ruta):
        """ Establecer la ruta al documento, entrega el distrito y la autoridad """
        self.ruta = ruta
        self.directorio, self.archivo = os.path.split(ruta)
        if '/' in self.directorio:
            separados = self.directorio.split('/')
            self.distrito = separados[0]
            self.autoridad = separados[1]
        else:
            self.distrito = None
            self.autoridad = None
        return(self.distrito, self.autoridad)

    def crear_identificador(self):
        """ Entrega el identificador del documento """
        if self.distrito is None or self.autoridad is None or self.archivo is None:
            raise Exception('ERROR: Falta el distrito, la autoridad o el archivo.')
        cadena = f'{self.distrito}|{self.autoridad}|{self.archivo}'
        self.identificador = hashlib.sha256(self.config.salt.encode() + cadena.encode()).hexdigest()
        return(self.identificador)

    def crear_acuse(self):
        """ Entrega el Acuse del documento """
        if self.distrito is None or self.autoridad is None or self.archivo is None:
            raise Exception('ERROR: Falta el distrito, la autoridad o el archivo.')
        if self.identificador is None:
            self.crear_identificador()
        self.acuse = Acuse(self.config)
        self.acuse.crear_asunto()
        self.acuse.crear_contenido(
            identificador=self.identificador,
            distrito=self.distrito,
            autoridad=self.autoridad,
            archivos=[self.archivo],
        )
        return(self.acuse)

    def enviar_acuse(self, destinatario_email):
        """ Enviar acuse vía correo electrónico """
        self.acuse.enviar(destinatario_email)

    def __repr__(self):
        return(f'<Documento> Ruta: {self.ruta}')
