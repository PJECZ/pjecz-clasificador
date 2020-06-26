import os
from depositos.documento import Documento


class Deposito(object):
    """ Depósito es un lugar de almacenamiento de documentos """

    def __init__(self, config):
        self.config = config
        self.documentos = []
        self.cantidad = 0
        self.rastreado = False

    def rastrear_recursivo(self, ruta):
        """ Rastrear de forma recursiva todos los documentos que tengan la fecha dada """
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield from self.rastrear_recursivo(item.path)
            elif (item.name.endswith('.pdf') or item.name.endswith('.PDF')) and item.name.startswith(self.config.fecha):
                yield item.path[len(self.config.deposito_ruta) + 1:]

    def rastrear(self):
        """ Rastrear los documentos en el depósito, entrega el lista de Documentos """
        if self.rastreado is False:
            if not os.path.exists(self.config.deposito_ruta):
                raise Exception('ERROR: No existe deposito_ruta.')
            for ruta in list(self.rastrear_recursivo(self.config.deposito_ruta)):
                documento = Documento(self.config)
                documento.establecer_ruta(ruta)
                self.documentos.append(documento)
            self.cantidad = len(self.documentos)
            self.rastreado = True
        return(self.documentos)

    def agregar_documento(self, adjunto):
        """ Agregar un documento al depósito """
        documento = Documento(self.config)
        documento.distrito = ''
        documento.autoridad = ''
        documento.archivo = ''
        self.documentos.append(documento)
        return(documento)

    def __repr__(self):
        """
        if deposito.cantidad == 0:
            click.echo(f'AVISO: No se encontraron documentos con fecha {config.fecha}')
        else:
            for documento in deposito.documentos:
                click.echo(documento.ruta)
        """
        return(f'<Deposito> Ruta: {self.config.deposito_ruta}')
