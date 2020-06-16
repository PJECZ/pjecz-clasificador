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
        """ Obtener de forma recursiva todos los documentos que tengan la fecha dada """
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield from self.rastrear_recursivo(item.path)
            elif (item.name.endswith('.pdf') or item.name.endswith('.PDF')) and item.name.startswith(self.config.fecha):
                yield item.path[len(self.config.deposito_ruta) + 1:]

    def rastrear(self):
        """ Obtener los documentos en el depósito """
        if self.rastreado is False:
            if not os.path.exists(self.config.deposito_ruta):
                raise Exception('ERROR: No existe deposito_ruta.')
            for ruta in list(self.rastrear_recursivo(self.config.deposito_ruta)):
                self.documentos.append(Documento(self.config, ruta))
            self.cantidad = len(self.documentos)
            self.rastreado = True
        return(self.documentos)

    def __repr__(self):
        return('<Deposito>')
