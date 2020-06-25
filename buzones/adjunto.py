import os
from datetime import datetime
from funciones.funciones import mes_en_palabra, hoy_dia_mes_ano


class Adjunto(object):
    """ Archivo adjunto en un mensaje """

    def __init__(self, config, archivo, contenido_tipo, contenido_binario):
        self.config = config
        self.archivo = archivo
        self.contenido_tipo = contenido_tipo
        self.contenido_binario = contenido_binario
        self.directorio = None
        self.ruta = None
        self.ya_guardado = False
        self.ruta_completa = None

    def establecer_ruta(self, ruta):
        """ Establecer la ruta relativa distrito/autoridad/año/mes/archivo donde guardarlo """
        try:
            datetime.strptime(self.archivo[0:10], '%Y-%m-%d')
            ano = self.archivo[0:4]
            mes = mes_en_palabra(int(self.archivo[5:7]))
            dia = self.archivo[8:10]
        except ValueError:
            dia, mes, ano = hoy_dia_mes_ano()
        self.directorio = f'{ruta}/{ano}/{mes}'
        self.ruta = f'{self.directorio}/{self.archivo}'
        return(self.ruta)

    def guardar(self):
        """ Guardar el archivo adjunto, entrega verdadero de tener éxito """
        if self.ya_guardado:
            return()
        if self.ruta is None:
            raise Exception('ERROR: No hay ruta definida para guardar el adjunto.')
        directorio_completo = self.config.deposito_ruta + '/' + self.directorio
        try:
            if not os.path.exists(directorio_completo):
                os.makedirs(directorio_completo)
        except Exception:
            raise Exception(f'ERROR: Al tratar de crear el directorio {directorio_completo}')
        self.ruta_completa = os.path.join(directorio_completo, self.archivo)
        try:
            with open(self.ruta_completa, 'wb') as puntero:
                puntero.write(self.contenido_binario)
        except Exception:
            raise Exception(f'ERROR: Al tratar de guardar {self.ruta_completa}')
        self.ya_guardado = True
        return(self.ya_guardado)

    def __repr__(self):
        if self.ya_guardado:
            return(f'<Adjunto> Guardado en: {self.ruta_completa}')
        elif self.ruta is None:
            return(f'<Adjunto> Tipo: {self.contenido_tipo}, Nombre: {self.archivo}')
        else:
            return(f'<Adjunto> Tipo: {self.contenido_tipo}, Ruta: {self.ruta}')
