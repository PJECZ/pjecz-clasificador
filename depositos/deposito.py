import os
from depositos.documento import Documento


class Deposito(object):
    """ Depósito es un lugar de almacenamiento de documentos """

    def __init__(self, config):
        self.config = config
        self.documentos = []
        self.ya_rastreado = False
        self.ya_respondidos = False

    def rastrear_recursivo(self, ruta):
        """ Rastrear de forma recursiva todos los documentos que tengan la fecha dada """
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield from self.rastrear_recursivo(item.path)
            elif (item.name.endswith('.pdf') or item.name.endswith('.PDF')):
                yield item.path[len(self.config.deposito_ruta) + 1:]

    def rastrear(self):
        """ Rastrear los documentos en el depósito, entrega el lista de Documentos """
        if self.ya_rastreado is False:
            if not os.path.exists(self.config.deposito_ruta):
                raise Exception('ERROR: No existe deposito_ruta.')
            for ruta in list(self.rastrear_recursivo(self.config.deposito_ruta)):
                documento = Documento(self.config)
                documento.establecer_ruta(ruta)
                if self.config.fecha != '' and documento.fecha != self.config.fecha:
                    continue
                if self.config.distrito != '' and documento.distrito != self.config.distrito:
                    continue
                if self.config.autoridad != '' and documento.autoridad != self.config.autoridad:
                    continue
                self.documentos.append(documento)
            self.ya_rastreado = True
        return(self.documentos)

    def responder_con_acuses(self, destinatarios):
        """ Responder con acuses """
        if self.ya_rastreado is False:
            self.rastrear()
        if self.ya_respondidos is False:
            for documento in self.documentos:
                destinatarios_dict = destinatarios.filtrar_con_archivo_ruta(documento.ruta)
                if len(destinatarios_dict) > 0:
                    for email, informacion in destinatarios_dict.items():
                        documento.enviar_acuse(email)
                else:
                    pass  # No hay destinatarios para la ruta
            self.ya_respondidos = True

    def __repr__(self):
        if len(self.documentos) > 0:
            documentos_repr = '\n  '.join([repr(documento) for documento in self.documentos])
            if self.ya_respondidos:
                return('<Deposito> Respondidos {}\n  {}'.format(len(self.documentos), documentos_repr))
            elif self.ya_rastreado:
                return('<Deposito> Rastreados {}\n  {}'.format(len(self.documentos), documentos_repr))
            else:
                return('<Deposito> Cantidad de documentos {}'.format(len(self.documentos)))
        else:
            return('<Deposito>')
