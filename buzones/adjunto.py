"""
Buzones, Adjunto
"""
from datetime import datetime, date, timedelta
import os
import logging
from pathlib import Path
import re
from unidecode import unidecode

from comunes.funciones import mes_en_palabra, hoy_dia_mes_ano

bitacora = logging.getLogger(__name__)
bitacora.setLevel(logging.INFO)
formato = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")
empunadura = logging.FileHandler("buzones.log")
empunadura.setFormatter(formato)
bitacora.addHandler(empunadura)


class Adjunto:
    """Archivo adjunto en un mensaje"""

    def __init__(self, config, archivo, contenido_tipo, contenido_binario):
        """Inicializar"""
        self.config = config
        self.archivo = archivo
        self.contenido_tipo = contenido_tipo
        self.contenido_binario = contenido_binario
        self.directorio = None
        self.ruta = None
        self.ya_guardado = False
        self.ruta_completa = None
        hoy = date.today()
        self.hoy_dt = datetime(year=hoy.year, month=hoy.month, day=hoy.day)
        self.limite_dt = self.hoy_dt + timedelta(days=-self.config.dias_limite)
        self.letras_digitos_regex = re.compile("[^0-9a-zA-Z]+")
        self.rechazo_mensaje = None

    def establecer_ruta(self, cliente_ruta):
        """Establecer la ruta relativa distrito/autoridad/año/mes/archivo donde guardarlo"""
        try:
            datetime.strptime(self.archivo[0:10], "%Y-%m-%d")
            ano = self.archivo[0:4]
            mes = mes_en_palabra(int(self.archivo[5:7]))
            dia = self.archivo[8:10]
        except ValueError:
            dia, mes, ano = hoy_dia_mes_ano()
        self.directorio = f"{cliente_ruta}/{ano}/{mes}"
        self.ruta = f"{self.directorio}/{self.archivo}"
        return self.ruta

    def guardar(self):
        """Guardar el archivo adjunto, entrega verdadero de tener éxito"""
        if self.ya_guardado is False:
            # Validar ruta
            if self.ruta is None:
                raise Exception("ERROR: No hay ruta definida para guardar el adjunto.")
            # Validar tipo de archivo
            if self.contenido_tipo not in self.config.contenidos_tipos:
                bitacora.warning("[%s] Se omite %s por ser %s", self.config.rama, self.archivo, self.contenido_tipo)
                self.rechazo_mensaje = "El archivo no es del tipo correcto. Debe ser de tipo pdf."
                raise AdjuntoRechazo(self.rechazo_mensaje)
            # Crear directorio para almacenar
            directorio_completo = self.config.deposito_ruta + "/" + self.directorio
            try:
                if not os.path.exists(directorio_completo):
                    os.makedirs(directorio_completo)
            except Exception:
                bitacora.error("[%s] Falló al crear el directorio %s", self.config.rama, directorio_completo)
                self.rechazo_mensaje = "Falló la creación del directorio para almacenar. Favor de reportar."
                raise AdjuntoRechazo(self.rechazo_mensaje)
            # Validar que tenga extensión PDF
            archivo_ruta = Path(self.archivo)
            if archivo_ruta.suffix.lower() != ".pdf":
                bitacora.error("[%s] Se omite %s por no tener la extensión pdf")
                self.rechazo_mensaje = "El archivo no tiene la extensión pdf."
                raise AdjuntoRechazo(self.rechazo_mensaje)
            # Validar fecha
            nombre_sin_extension = unidecode(archivo_ruta.name[:-4])
            elementos = re.sub(self.letras_digitos_regex, "-", nombre_sin_extension).strip("-").split("-")
            try:
                ano = int(elementos[0])
                mes = int(elementos[1])
                dia = int(elementos[2])
                fecha = date(ano, mes, dia)
            except (IndexError, ValueError):
                bitacora.error("[%s] Se omite %s por que la fecha es incorrecta", self.config.rama, self.archivo)
                raise AdjuntoRechazo("La fecha es incorrecta. El nombre del archivo debe comenzar con los 4 dígitos del año, 2 del mes y 2 del día separados por guiones.")
            # Validar que la fecha esté en el rango correcto
            if not self.limite_dt <= datetime(year=fecha.year, month=fecha.month, day=fecha.day) <= self.hoy_dt:
                bitacora.error("[%s] Se omite %s por que la fecha está fuera de rango", self.config.rama, self.archivo)
                raise AdjuntoRechazo("La fecha está fuera de rango. No se permiten fechas en el futuro ni muy antiguas.")
            # Escribir el archivo
            self.ruta_completa = os.path.join(directorio_completo, self.archivo)
            try:
                with open(self.ruta_completa, "wb") as puntero:
                    puntero.write(self.contenido_binario)
            except Exception:
                bitacora.error("[%s] Falló al escribir %s", self.config.rama, self.ruta_completa)
                raise AdjuntoRechazo("Falló la escritura del archivo. Favor de reportar.")
            # Mensaje de éxito
            self.ya_guardado = True
            bitacora.info("[%s] Guardado en %s", self.config.rama, self.ruta)
            return True

    def __repr__(self):
        """Representación"""
        if self.ya_guardado:
            return f"<Adjunto> Tipo: {self.contenido_tipo}, Guardado en: {self.ruta_completa}"
        elif self.ruta is None:
            return f"<Adjunto> Tipo: {self.contenido_tipo}, Archivo: {self.archivo}"
        else:
            return f"<Adjunto> Tipo: {self.contenido_tipo}, Ruta: {self.ruta}"


class AdjuntoRechazo(Exception):
    """Se rechaza el archivo adjunto"""
