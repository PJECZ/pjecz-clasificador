import os


class Deposito(object):
    """ Depósito es un lugar de almacenamiento de documentos """

    def __init__(self, config):
        self.config = config
        self.archivos = []
        self.rastreado = False

    def rastrear_recursivo(self, ruta):
        """ Obtener de forma recursiva todos los PDF que tengan la fecha dada """
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield from self.rastrear_recursivo(item.path)
            elif (item.name.endswith('.pdf') or item.name.endswith('.PDF')) and item.name.startswith(self.config.fecha):
                yield item.path[len(self.config.deposito_ruta) + 1:]

    def rastrear(self):
        """ Obtener los archivos en el depósito """
        if self.rastreado == False:
            if not os.path.exists(self.config.deposito_ruta):
                raise Exception('ERROR: No existe deposito_ruta.')
            self.archivos = self.rastrear_recursivo(self.config.deposito_ruta)
            self.rastreado = True
        return(self.archivos)

    def __repr__(self):
        return('<Deposito>')
