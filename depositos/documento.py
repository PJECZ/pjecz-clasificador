"""
Documento
"""
import hashlib
import os
from comunes.funciones import validar_fecha
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
        self.fecha = None
        self.identificador = None
        self.acuses = []
        self.ya_enviado = False

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
        try:
            self.fecha = validar_fecha(self.archivo[:10])
        except Exception:
            self.fecha = None
        return self.distrito, self.autoridad

    def crear_identificador(self):
        """ Entrega el identificador del documento """
        if self.ruta is None or self.directorio is None or self.archivo is None:
            raise Exception('ERROR: Falta definir la ruta, directorio y/o archivo.')
        if self.distrito is None or self.autoridad is None:
            raise Exception('ERROR: Falta definir el distrito y/o autoridad.')
        cadena = f'{self.distrito}|{self.autoridad}|{self.archivo}'
        self.identificador = hashlib.sha256(self.config.salt.encode() + cadena.encode()).hexdigest()
        return self.identificador

    def enviar_acuse(self, email):
        """ Enviar acuse vía correo electrónico """
        if self.ruta is None or self.directorio is None or self.archivo is None:
            raise Exception('ERROR: Falta definir la ruta, directorio y/o archivo.')
        if self.distrito is None or self.autoridad is None:
            raise Exception('ERROR: Falta definir el distrito y/o autoridad.')
        if self.ya_enviado is False:
            acuse = Acuse(self.config)
            acuse.crear_asunto()
            acuse.crear_contenido(
                identificador=self.crear_identificador(),
                distrito=self.distrito,
                autoridad=self.autoridad,
                archivos=[self.archivo],
            )
            acuse.enviar(email)
            self.acuses.append(acuse)
            self.ya_enviado = True

    def __repr__(self):
        if self.ya_enviado:
            acuses_repr = '\n    '.join([repr(acuse) for acuse in self.acuses])
            return '<Documento> Enviado Ruta: {}\n    {}'.format(self.ruta, acuses_repr)
        elif self.ruta is None:
            return '<Documento>'
        else:
            return '<Documento> Ruta: {}'.format(self.ruta)
