import click
import configparser
import os
import sys
from datetime import datetime, date
from tabulate import tabulate

from clientes.clientes import Clientes
from depositos.acuse import Acuse
from depositos.deposito import Deposito


class Config(object):

    def __init__(self):
        self.fecha = str(date.today())
        self.rama = ''
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


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--fecha', default='', type=str, help='Fecha AAAA-MM-DD')
@click.option('--rama', default='', type=str, help='Acuerdos, Edictos o Sentencias')
@pass_config
def cli(config, fecha, rama):
    click.echo('Hola, ¡soy Clasificador!')
    # Fecha
    if fecha != '':
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            config.fecha = fecha
        except ValueError:
            click.echo('ERROR: Fecha incorrecta.')
            sys.exit(1)
    # Rama
    config.rama = rama.title()
    if config.rama not in ('Acuerdos', 'Edictos', 'Sentencias'):
        click.echo('ERROR: Rama no programada.')
        sys.exit(1)
    # Configuración
    settings = configparser.ConfigParser()
    settings.read('settings.ini')
    try:
        config.servidor_imap = settings['Global']['servidor_imap']
        config.servidor_smtp = settings['Global']['servidor_smtp']
        config.deposito_ruta = settings[config.rama]['deposito_ruta']
        config.email_direccion = settings[config.rama]['email_direccion']
        config.email_contrasena = settings[config.rama]['email_contrasena']
        if 'google_sheets_api_spreadsheet_id' in settings[config.rama]:
            config.google_sheets_api_spreadsheet_id = settings[config.rama]['google_sheets_api_spreadsheet_id']
        if 'google_sheets_api_rango' in settings[config.rama]:
            config.google_sheets_api_rango = settings[config.rama]['google_sheets_api_rango']
        if 'google_sheets_api_columna_autoridad' in settings[config.rama]:
            config.google_sheets_api_columna_autoridad = int(settings[config.rama]['google_sheets_api_columna_autoridad'])
        if 'google_sheets_api_columna_distrito' in settings[config.rama]:
            config.google_sheets_api_columna_distrito = int(settings[config.rama]['google_sheets_api_columna_distrito'])
        if 'google_sheets_api_columna_email' in settings[config.rama]:
            config.google_sheets_api_columna_email = int(settings[config.rama]['google_sheets_api_columna_email'])
        if 'google_sheets_api_columna_ruta' in settings[config.rama]:
            config.google_sheets_api_columna_ruta = int(settings[config.rama]['google_sheets_api_columna_ruta'])
        if 'remitentes_csv_ruta' in settings[config.rama]:
            config.remitentes_csv_ruta = settings[config.rama]['remitentes_csv_ruta']
        if 'remitentes_csv_columna_distrito' in settings[config.rama]:
            config.remitentes_csv_columna_distrito = settings[config.rama]['remitentes_csv_columna_distrito']
        if 'remitentes_csv_columna_autoridad' in settings[config.rama]:
            config.remitentes_csv_columna_autoridad = settings[config.rama]['remitentes_csv_columna_autoridad']
        if 'remitentes_csv_columna_email' in settings[config.rama]:
            config.remitentes_csv_columna_email = settings[config.rama]['remitentes_csv_columna_email']
        if 'remitentes_csv_columna_ruta' in settings[config.rama]:
            config.remitentes_csv_columna_ruta = settings[config.rama]['remitentes_csv_columna_ruta']
    except KeyError:
        click.echo('ERROR: Falta configuración en settings.ini')
        sys.exit(1)


@cli.command()
@pass_config
def informar(config):
    """ Informar con una línea breve en pantalla """
    click.echo('Voy a informar...')
    # Mostrar información
    click.echo(f'Rama:     {config.rama}')
    click.echo(f'Fecha:    {config.fecha}')
    click.echo(f'e-mail:   {config.email_direccion}')
    click.echo(f'Depósito: {config.deposito_ruta}')
    # Mostrar clientes
    clientes = Clientes(config)
    destinatarios = clientes.alimentar()
    tabla = [['e-mail', 'Mover a']]
    for email, informacion in destinatarios.items():
        tabla.append([email, informacion['ruta']])
    click.echo(tabulate(tabla, headers='firstrow'))
    sys.exit(0)


@cli.command()
@pass_config
def rastrear(config):
    """ Rastrear archivos en la rama y fecha dada """
    click.echo('Voy a rastrear...')
    click.echo(f'Fecha: {config.fecha}')
    # Mostrar los archivos encontrados en el depósito
    deposito = Deposito(config)
    for item in deposito.rastrear():
        click.echo(item)
    sys.exit(0)


@cli.command()
@click.option('--enviar', default=False, help='Enviar los mensajes')
@pass_config
def responder(config, enviar):
    """ Responder con un mensaje vía correo electrónico """
    click.echo('Voy a rastrear y responder...')
    # Alimentar clientes
    clientes = Clientes(config)
    clientes.alimentar()
    # Rastrear el depósito
    deposito = Deposito(config)
    archivos = deposito.rastrear()
    # Mostrar en pantalla
    for archivo in archivos:
        destinatarios = clientes.filtrar_con_archivo_ruta(archivo)
        if len(destinatarios) == 0:
            click.echo(f'AVISO: No hay destinatarios para {archivo}')
        else:
            click.echo(f'Para {archivo}')
            for email, informacion in destinatarios.items():
                if enviar:
                    click.echo(f"- Enviando a {informacion['autoridad']} <{email}>")
                    acuse = Acuse(config)
                    acuse.elaborar_asunto()
                    acuse.elaborar_contenido(
                        identificador='123123',
                        autoridad=informacion['autoridad'],
                        distrito=informacion['distrito'],
                        archivos=[os.path.basename(archivo)],
                    )
                    acuse.enviar(email, 'Constancia de Publicación')
                else:
                    click.echo(f"- SIMULO que es para {informacion['autoridad']} <{email}>")
    # Enviar mensajes
    sys.exit(0)


cli.add_command(informar)
cli.add_command(rastrear)
cli.add_command(responder)
