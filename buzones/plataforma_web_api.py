"""
Plataforma Web API
"""
from datetime import datetime
import requests

API_BASE = "https://plataforma-web-api-dot-pjecz-268521.uc.r.appspot.com"
STORAGE_BASE = "https://storage.googleapis.com/pjecz-consultas/Listas de Acuerdos"
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


class PlataformaWebApi:
    """ Plataforma Web API """

    def __init__(self, config, remitentes):
        """ Inicializar """
        self.config = config
        self.remitentes = remitentes

    def obtener_autoridad_id(self):
        """ Obtener autoridad_id """
        autoridad_id = 38  # Juzgado Primero de Primera Instancia en Materia Mercantil Saltillo
        # autoridad_llamado = requests.get(f"{API_BASE}/autoridades/{autoridad_id}", timeout=16)
        # autoridad = autoridad_llamado.json()
        # print("  autoridad_id:", autoridad["id"], autoridad["descripcion"])
        return autoridad_id

    def obtener_fecha(self):
        """ Obtener la fecha como YYYY-MM-DD """
        hoy = datetime.now()  # Hoy
        fecha = hoy.strftime("%Y-%m-%d")
        return fecha

    def obtener_archivo(self, adjunto):
        """ Obtener nombre.extension del archivo """
        # archivo = f"{fecha}-lista-de-acuerdos.pdf"
        return adjunto.archivo

    def obtener_descripcion(self):
        """ Obtener descripción """
        return "Lista de Acuerdos"

    def obtener_url(self):
        """ Obtener URL """
        hoy = datetime.now()  # Hoy
        fecha = hoy.strftime("%Y-%m-%d")
        ano = str(hoy.year)
        mes = MESES[hoy.month]
        url = f"{STORAGE_BASE}/{autoridad['directorio_listas_de_acuerdos']}/{ano}/{mes}/{archivo}"
        return url

    def mandar(self, mensaje):
        """ Mandar a la API la(s) orden(es) de postear """
        if self.config.rama != "acuerdos":
            return
        carga = {
            "autoridad_id": autoridad_id,
            "fecha": fecha,
            "archivo": archivo,
            "descripcion": descripcion,
            "url": url,
        }
        listas_de_acuerdos_llamado = requests.post(f"{API_BASE}/listas_de_acuerdos/nuevo", json=carga, timeout=16)
        # listas_de_acuerdos_llamado.status_code


"""
    self.config.rama
    self.remitentes
    self.remitentes[email]['distrito'] <- str
    self.remitentes[email]['autoridad'] <- str
    self.remitentes[email]['ruta']
    self.mensaje.email
    self.mensaje.adjuntos
    self.mensaje.adjuntos[0].archivo
    self.mensaje.adjuntos[0].directorio = f'{cliente_ruta}/{ano}/{mes}'
    self.mensaje.adjuntos[0].ruta = f'{self.directorio}/{self.archivo}'
    self.mensaje.adjuntos[0].ya_guardado = True
"""
