import click
import configparser
import email
import email.message
import imaplib
import os
import smtplib
import time
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Config(object):

    def __init__(self):
        self.rama = ''
        self.servidor_imap = ''
        self.email_direccion = ''
        self.email_contrasena = ''
        self.deposito_ruta = ''


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--rama', default='', type=str, help='Acuerdos, Edictos o Sentencias')
@pass_config
def cli(config, rama):
    click.echo('Hola, ¡soy Clasificador!')
    # Rama
    if not rama.title() in ['Acuerdos', 'Edictos', 'Sentencias']:
        click.echo('ERROR: Rama no programada.')
        sys.exit(1)
    config.rama = rama.title()
    # Configuración
    settings = configparser.ConfigParser()
    settings.read('settings.ini')
    try:
        config.servidor_imap = settings['Global']['servidor_imap']
        config.email_direccion = settings[config.rama]['email_direccion']
        config.email_contrasena = settings[config.rama]['email_contrasena']
        config.deposito_ruta = settings[config.rama]['deposito_ruta']
    except KeyError:
        click.echo('ERROR: Falta configuración en settings.ini')
        sys.exit(1)


@cli.command()
@pass_config
def informar(config):
    """ Informar con una línea breve en pantalla """
    click.echo('Voy a informar... nada aun.')


@cli.command()
@pass_config
def leer(config):
    """ Leer """
    click.echo('Voy a leer...')
    # Obtener mensajes sin leer
    mail = imaplib.IMAP4_SSL(config.servidor_imap)
    mail.login(config.email_direccion, config.email_contrasena)
    mail.list()
    # Acceso a la carpeta inbox con permisos de lectura
    mail.select('inbox')
    type, data = mail.search(None, 'UNSEEN') # busca los correos que no han sido leido
    mail_ids = data[0]
    id_list = mail_ids.split()
    # Recorre los correos por id
    for num in data[0].split():
        latest_email_uid = id_list[-1]
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
        latest_email_uid = id_list[-1]
        # Converts byte literal to string removing b''
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        # Mostrar
        click.echo(f'To:      {email_message["To"]}')
        click.echo(f'From:    {email_message["From"]}')
        click.echo(f'Subject: {email_message["Subject"]}')
        click.echo(f'Date:    {email_message["Date"]}')
        click.echo()


@cli.command()
@pass_config
def leer_clasificar(config):
    """ Leer y clasificar """
    click.echo('Voy a leer y clasificar... nada aun.')


@cli.command()
@pass_config
def leer_clasificar_responder(config):
    """ Leer, clasificar y responder """
    click.echo('Voy a leer, clasificar y responder... nada aun.')


cli.add_command(informar)
cli.add_command(leer)
cli.add_command(leer_clasificar)
cli.add_command(leer_clasificar_responder)
