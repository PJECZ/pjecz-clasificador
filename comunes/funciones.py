"""
Funciones
"""
from datetime import date, datetime


MESES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
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
