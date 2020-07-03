import logging
import os
from datetime import datetime
from comunes.funciones import mes_en_palabra, hoy_dia_mes_ano


bitacora = logging.getLogger(__name__)
bitacora.setLevel(logging.INFO)
formato = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
empunadura = logging.FileHandler('buzones.log')
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)


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

    def establecer_ruta(self, cliente_ruta):
        """ Establecer la ruta relativa distrito/autoridad/año/mes/archivo donde guardarlo """
        try:
            datetime.strptime(self.archivo[0:10], '%Y-%m-%d')
            ano = self.archivo[0:4]
            mes = mes_en_palabra(int(self.archivo[5:7]))
            dia = self.archivo[8:10]
        except ValueError:
            dia, mes, ano = hoy_dia_mes_ano()
        self.directorio = f'{cliente_ruta}/{ano}/{mes}'
        self.ruta = f'{self.directorio}/{self.archivo}'
        return(self.ruta)

    def guardar(self):
        """ Guardar el archivo adjunto, entrega verdadero de tener éxito """
        if self.ya_guardado is False:
            if self.ruta is None:
                raise Exception('ERROR: No hay ruta definida para guardar el adjunto.')
            if self.contenido_tipo not in self.config.contenidos_tipos:
                bitacora.warning('[{}] Debería omitir {} por ser {}'.format(self.config.rama, self.archivo, self.contenido_tipo))
            directorio_completo = self.config.deposito_ruta + '/' + self.directorio
            try:
                if not os.path.exists(directorio_completo):
                    os.makedirs(directorio_completo)
            except Exception:
                bitacora.error('[{}] Falló al crear el directorio {}'.format(self.config.rama, directorio_completo))
                return(False)
            self.ruta_completa = os.path.join(directorio_completo, self.archivo)
            try:
                with open(self.ruta_completa, 'wb') as puntero:
                    puntero.write(self.contenido_binario)
            except Exception:
                bitacora.error('[{}] Falló al escribir {}'.format(self.config.rama, self.ruta_completa))
                return(False)
            self.ya_guardado = True
            bitacora.info('[{}] Guardado en {}'.format(self.config.rama, self.ruta))
            return(True)

    def __repr__(self):
        if self.ya_guardado:
            return(f'<Adjunto> Tipo: {self.contenido_tipo}, Guardado en: {self.ruta_completa}')
        elif self.ruta is None:
            return(f'<Adjunto> Tipo: {self.contenido_tipo}, Archivo: {self.archivo}')
        else:
            return(f'<Adjunto> Tipo: {self.contenido_tipo}, Ruta: {self.ruta}')
