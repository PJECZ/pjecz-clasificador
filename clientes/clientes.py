import csv
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class Clientes(object):
    """ Clientes se alimenta desde un CSV o una hoja de Google Sheet, entrega un diccionario con clave e-mail """

    def __init__(self, config):
        self.config = config
        self.clientes = {}
        self.alimentado = False

    def alimentar_desde_archivo_csv(self):
        """ Cargar los clientes desde el archivo CSV """
        self.clientes = {}
        if os.path.exists(self.config.remitentes_csv_ruta):
            with open(self.config.remitentes_csv_ruta) as puntero:
                lector = csv.DictReader(puntero)
                for renglon in lector:
                    if renglon[self.config.remitentes_csv_columna_email] != '' and renglon[self.config.remitentes_csv_columna_ruta] != '':
                        self.clientes[renglon[self.config.remitentes_csv_columna_email]] = {
                            'distrito': renglon[self.config.remitentes_csv_columna_distrito],
                            'autoridad': renglon[self.config.remitentes_csv_columna_autoridad],
                            'ruta': renglon[self.config.remitentes_csv_columna_ruta],
                        }
        return(self.clientes)

    def alimentar_desde_google_sheets_api(self):
        """ Cargar los clientes desde Google Sheets """
        # Google Sheets API
        # https://developers.google.com/sheets/api/quickstart/python
        creds = None
        # En el archivo token.pickle se guardan el acceso y tokens
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # Si no hay credenciales guardadas o si no son válidas
        if not creds or not creds.valid:
            # Si expiraron
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Conservar las credenciales para la próxima ejecución
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        # Llamar a la API de Google Sheets
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.config.google_sheets_api_spreadsheet_id, range=self.config.google_sheets_api_rango).execute()
        values = result.get('values', [])
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
                    self.clientes[email] = {
                        'distrito': distrito,
                        'autoridad': autoridad,
                        'ruta': ruta,
                    }
        return(self.clientes)

    def alimentar(self):
        """ Cargar los clientes """
        self.alimentado = True
        if self.config.remitentes_csv_ruta != '':
            return(self.alimentar_desde_archivo_csv())
        elif self.config.google_sheets_api_spreadsheet_id != '':
            return(self.alimentar_desde_google_sheets_api())
        else:
            raise Exception('ERROR: No se pueden cargar los clientes por configuración incompleta.')

    def filtrar_con_archivo_ruta(self, archivo_ruta):
        """ Filtrar los clientes donde ruta sea el inicio de archivo_ruta """
        if self.alimentado is False:
            self.alimentar()
        filtrados = {}
        for email, informacion in self.clientes.items():
            if archivo_ruta.startswith(informacion['ruta']):
                filtrados[email] = {
                    'distrito': informacion['distrito'],
                    'autoridad': informacion['autoridad'],
                    'ruta': informacion['ruta'],
                }
        return(filtrados)

    def __repr__(self):
        return('<Clientes>')
