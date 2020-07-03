import click
import configparser
from datetime import date


class Config(object):

    def __init__(self):
        self.rama = ''
        self.distrito = ''  # Filtro
        self.autoridad = ''  # Filtro
        self.fecha = str(date.today())  # Filtro
        self.contenidos_tipos = ''
        self.email_desarrollo = ''
        self.salt = ''
        self.servidor_imap = ''
        self.servidor_smtp = ''
        self.buzones_acuse_asunto = ''
        self.buzones_acuse_contenido = ''
        self.deposito_ruta = ''
        self.depositos_acuse_asunto = ''
        self.depositos_acuse_contenido = ''
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
        if self.rama == '':
            raise Exception('ERROR: Faltó definir la rama.')
        settings = configparser.ConfigParser()
        settings.read('settings.ini')
        try:
            self.contenidos_tipos = settings['global']['contenidos_tipos'].split(',')
            if 'email_desarrollo' in settings['global']:
                self.email_desarrollo = settings['global']['email_desarrollo']
            self.salt = settings['global']['salt']
            self.servidor_imap = settings['global']['servidor_imap']
            self.servidor_smtp = settings['global']['servidor_smtp']
            if 'buzones_acuse_asunto' in settings[self.rama]:
                self.buzones_acuse_asunto = settings[self.rama]['buzones_acuse_asunto']
            if 'buzones_acuse_contenido' in settings[self.rama]:
                self.buzones_acuse_contenido = settings[self.rama]['buzones_acuse_contenido']
            self.deposito_ruta = settings[self.rama]['deposito_ruta']
            if 'depositos_acuse_asunto' in settings[self.rama]:
                self.depositos_acuse_asunto = settings[self.rama]['depositos_acuse_asunto']
            if 'depositos_acuse_contenido' in settings[self.rama]:
                self.depositos_acuse_contenido = settings[self.rama]['depositos_acuse_contenido']
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
            raise Exception(f'ERROR: Falta configuración en settings.ini para la rama {self.rama}')


pass_config = click.make_pass_decorator(Config, ensure=True)
