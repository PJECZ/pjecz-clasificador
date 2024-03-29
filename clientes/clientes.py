"""
Clientes
"""
import csv
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tabulate import tabulate

# Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


class Clientes:
    """ Clientes se alimenta desde un CSV o una hoja de Google Sheet, entrega un diccionario con clave e-mail """

    def __init__(self, config):
        """ Inicializar """
        self.config = config
        self.clientes = {}
        self.alimentado = False

    def cargar_desde_archivo_csv(self):
        """ Cargar los clientes desde el archivo CSV """
        self.clientes = {}
        if os.path.exists(self.config.remitentes_csv_ruta):
            with open(self.config.remitentes_csv_ruta) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    try:
                        email = renglon[self.config.remitentes_csv_columna_email]
                        distrito = renglon[self.config.remitentes_csv_columna_distrito]
                        autoridad = renglon[self.config.remitentes_csv_columna_autoridad]
                        ruta = renglon[self.config.remitentes_csv_columna_ruta]
                    except IndexError:
                        pass
                    else:
                        if email != "" and distrito != "" and autoridad != "" and ruta != "":
                            self.clientes[email] = {
                                "distrito": distrito,
                                "autoridad": autoridad,
                                "ruta": ruta,
                            }
        return self.clientes

    def cargar_desde_google_sheets_api(self):
        """ Cargar los clientes desde Google Sheets """
        # Google Sheets API
        # https://developers.google.com/sheets/api/quickstart/python
        creds = None
        # En el archivo token.json se guardan el acceso y tokens
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # Si no hay credenciales guardadas o si no son válidas
        if not creds or not creds.valid:
            # Si expiraron
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # Conservar las credenciales para la próxima ejecución
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        values = None
        try:
            # Llamar a la API de Google Sheets
            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.config.google_sheets_api_spreadsheet_id, range=self.config.google_sheets_api_rango).execute()
            values = result.get("values", [])
        except HttpError as error:
            raise error
        # Entregar los clientes como un diccionario
        self.clientes = {}
        if values:
            for row in values:
                try:
                    email = row[self.config.google_sheets_api_columna_email]
                    distrito = row[self.config.google_sheets_api_columna_distrito]
                    autoridad = row[self.config.google_sheets_api_columna_autoridad]
                    ruta = row[self.config.google_sheets_api_columna_ruta]
                except IndexError:
                    pass
                else:
                    if email != "" and distrito != "" and autoridad != "" and ruta != "":
                        self.clientes[email] = {
                            "distrito": distrito,
                            "autoridad": autoridad,
                            "ruta": ruta,
                        }
        return self.clientes

    def cargar(self):
        """ Cargar los clientes """
        self.alimentado = True
        if self.config.remitentes_csv_ruta != "":
            self.cargar_desde_archivo_csv()
        elif self.config.google_sheets_api_spreadsheet_id != "":
            self.cargar_desde_google_sheets_api()
        else:
            raise Exception("ERROR: No se pueden cargar los clientes porque la configuración está incompleta.")
        if len(self.clientes) == 0:
            raise Exception("AVISO: No se cargó ningún cliente.")
        return self.clientes

    def filtrar_con_archivo_ruta(self, archivo_ruta):
        """ Filtrar los clientes donde ruta sea el inicio de archivo_ruta """
        if self.alimentado is False:
            self.cargar()
        filtrados = {}
        for email, informacion in self.clientes.items():
            if archivo_ruta.startswith(informacion["ruta"]):
                filtrados[email] = {
                    "distrito": informacion["distrito"],
                    "autoridad": informacion["autoridad"],
                    "ruta": informacion["ruta"],
                }
        return filtrados

    def crear_tabla(self):
        """ Crear tabla con Tabulate para mostrar en terminal """
        tabla = [["e-mail", "Mover a"]]
        for email, informacion in self.clientes.items():
            tabla.append([email, informacion["ruta"]])
        return tabulate(tabla, headers="firstrow")

    def __repr__(self):
        """ Representación """
        if self.alimentado is True:
            return "<Clientes> Hay {} clientes".format(len(self.clientes))
        return "<Clientes>"
