"""
Funciones
"""

from datetime import date, datetime
from pathlib import Path
import re
from unidecode import unidecode

MESES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def mes_en_palabra(mes_numero=None):
    """ Entrega el nombre del mes """
    if isinstance(mes_numero, int) and mes_numero in MESES:
        return MESES[mes_numero]
    hoy = date.today()
    return MESES[hoy.month]


def hoy_dia_mes_ano(fecha=None):
    """ Entrega el dia en dos digitos, el mes en palabra y el año en cuatro digitos """
    if fecha is None or fecha == "":
        fecha_date = date.today()
    else:
        fecha_date = datetime.strptime(fecha, "%Y-%m-%d")
    dia = "{:02d}".format(fecha_date.day)
    mes = mes_en_palabra(fecha_date.month)
    ano = str(fecha_date.year)
    return (dia, mes, ano)


def nombre_seguro_archivo(nombre_archivo):
    """Entrega un nombre de archivo seguro, solo con letras, dígitos y guiones"""

    # Separar el nombre del archivo de su extensión
    archivo_ruta = Path(nombre_archivo)
    nombre_sin_extension = archivo_ruta.stem
    extension = archivo_ruta.suffix.lower()

    # Normalizar con unidecode
    nombre_sin_extension = unidecode(nombre_sin_extension).strip()

    # Reemplazar caracteres no permitidos por guiones
    nombre_sin_extension = re.sub(r'[^a-zA-Z0-9-]', '-', nombre_sin_extension)

    # Eliminar dos o más guiones consecutivos
    nombre_sin_extension = re.sub(r'-{2,}', '-', nombre_sin_extension).strip('-')

    # Entregar el nombre seguro con la extensión original
    return f"{nombre_sin_extension}{extension}"


def validar_email(email=""):
    """ Validar email """
    return email


def validar_fecha(fecha=""):
    """ Validar una fecha """
    if fecha != "":
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as error:
            raise Exception("Fecha incorrecta.") from error
    return str(fecha)


def validar_rama(rama=""):
    """ Validar rama """
    return rama.lower()
