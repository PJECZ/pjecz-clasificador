import click
import configparser
from datetime import date


class Config(object):

    def __init__(self):
        self.email = ''
        self.fecha = str(date.today())
        self.rama = ''
        self.email_desarrollo = ''
        self.salt = ''
        self.servidor_imap = ''
        self.servidor_smtp = ''
        self.deposito_ruta = ''
        self.email_direccion = ''
        self.email_contrasena = ''
        self.google_sheets_api_spreadsheet_id = ''
        self.google_sheets_api_rango = ''
        self.google_sheets_api_columna_autoridad = ''
        self.google_sheets_api_columna_distrito = ''
        self.google_sheets_api_columna_email = ''
        self.google_sheets_api_columna_ruta = ''
        self.remitentes_csv_ruta = ''
        self.remitentes_csv_columna_distrito = ''
        self.remitentes_csv_columna_autoridad = ''
        self.remitentes_csv_columna_email = ''
        self.remitentes_csv_columna_ruta = ''

    def cargar_configuraciones(self):
        settings = configparser.ConfigParser()
        settings.read('settings.ini')
        try:
            if 'email_desarrollo' in settings['Global']:
                self.email_desarrollo = settings['Global']['email_desarrollo']
            self.salt = settings['Global']['salt']
            self.servidor_imap = settings['Global']['servidor_imap']
            self.servidor_smtp = settings['Global']['servidor_smtp']
            self.deposito_ruta = settings[self.rama]['deposito_ruta']
            self.email_direccion = settings[self.rama]['email_direccion']
            self.email_contrasena = settings[self.rama]['email_contrasena']
            if 'google_sheets_api_spreadsheet_id' in settings[self.rama]:
                self.google_sheets_api_spreadsheet_id = settings[self.rama]['google_sheets_api_spreadsheet_id']
            if 'google_sheets_api_rango' in settings[self.rama]:
                self.google_sheets_api_rango = settings[self.rama]['google_sheets_api_rango']
            if 'google_sheets_api_columna_autoridad' in settings[self.rama]:
                self.google_sheets_api_columna_autoridad = int(settings[self.rama]['google_sheets_api_columna_autoridad'])
            if 'google_sheets_api_columna_distrito' in settings[self.rama]:
                self.google_sheets_api_columna_distrito = int(settings[self.rama]['google_sheets_api_columna_distrito'])
            if 'google_sheets_api_columna_email' in settings[self.rama]:
                self.google_sheets_api_columna_email = int(settings[self.rama]['google_sheets_api_columna_email'])
            if 'google_sheets_api_columna_ruta' in settings[self.rama]:
                self.google_sheets_api_columna_ruta = int(settings[self.rama]['google_sheets_api_columna_ruta'])
            if 'remitentes_csv_ruta' in settings[self.rama]:
                self.remitentes_csv_ruta = settings[self.rama]['remitentes_csv_ruta']
            if 'remitentes_csv_columna_distrito' in settings[self.rama]:
                self.remitentes_csv_columna_distrito = settings[self.rama]['remitentes_csv_columna_distrito']
            if 'remitentes_csv_columna_autoridad' in settings[self.rama]:
                self.remitentes_csv_columna_autoridad = settings[self.rama]['remitentes_csv_columna_autoridad']
            if 'remitentes_csv_columna_email' in settings[self.rama]:
                self.remitentes_csv_columna_email = settings[self.rama]['remitentes_csv_columna_email']
            if 'remitentes_csv_columna_ruta' in settings[self.rama]:
                self.remitentes_csv_columna_ruta = settings[self.rama]['remitentes_csv_columna_ruta']
        except KeyError:
            raise Exception('ERROR: Falta configuración en settings.ini')


pass_config = click.make_pass_decorator(Config, ensure=True)
