from datetime import date


def mes_en_palabra(mes_numero=None):
    """ Entrega el nombre del mes """
    meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
    if isinstance(mes_numero, int) and mes_numero in meses:
        return(meses[mes_numero])
    else:
        hoy = date.today()
        return(meses[hoy.month])


def hoy_dia_mes_ano():
    hoy = date.today()
    dia = '{:02d}'.format(hoy.day)
    mes = mes_en_palabra(hoy.month)
    ano = str(hoy.year)
    return(dia, mes, ano)
