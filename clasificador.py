import click
import csv
import configparser
import email
import imaplib
import os
import smtplib
import sys
from datetime import datetime, date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tabulate import tabulate


class Config(object):

    def __init__(self):
        self.rama = ''
        self.notificar = ''
        self.servidor_imap = ''
        self.servidor_smtp = ''
        self.remitentes_csv_ruta = ''
        self.email_direccion = ''
        self.email_contrasena = ''
        self.deposito_ruta = ''


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@click.option('--rama', default='', type=str, help='Acuerdos, Edictos o Sentencias')
@click.option('--notificar', default='', type=str, help='Correo electrónico a quien notificar')
@pass_config
def cli(config, rama, notificar):
    click.echo('Hola, ¡soy Clasificador!')
    # Rama
    config.rama = rama.title()
    if not config.rama in ('Acuerdos', 'Edictos', 'Sentencias'):
        click.echo('ERROR: Rama no programada.')
        sys.exit(1)
    # Notificar
    config.notificar = notificar
    # Configuración
    settings = configparser.ConfigParser()
    settings.read('settings.ini')
    try:
        config.servidor_imap = settings['Global']['servidor_imap']
        config.servidor_smtp = settings['Global']['servidor_smtp']
        config.remitentes_csv_ruta = settings['Global']['remitentes_csv_ruta']
        config.email_direccion = settings[config.rama]['email_direccion']
        config.email_contrasena = settings[config.rama]['email_contrasena']
        config.deposito_ruta = settings[config.rama]['deposito_ruta']
    except KeyError:
        click.echo('ERROR: Falta configuración en settings.ini')
        sys.exit(1)
    # Validar
    if not config.servidor_imap:
        click.echo('ERROR: En settings.ini falta el servidor_imap')
        sys.exit(1)
    if not config.servidor_smtp:
        click.echo('ERROR: En settings.ini falta el servidor_smtp')
        sys.exit(1)
    if not config.remitentes_csv_ruta or not os.path.exists(config.remitentes_csv_ruta) or not os.path.isfile(config.remitentes_csv_ruta):
        click.echo('ERROR: En settings.ini no existe remitentes_csv_ruta')
        sys.exit(1)
    if not config.email_direccion:
        click.echo('ERROR: En settings.ini falta email_direccion')
        sys.exit(1)
    if not config.email_contrasena:
        click.echo('ERROR: En settings.ini falta email_contrasena')
        sys.exit(1)
    if not config.deposito_ruta:
        click.echo('ERROR: En settings.ini falta deposito_ruta')
        sys.exit(1)
    if not config.remitentes_csv_ruta or not os.path.exists(config.deposito_ruta) or not os.path.isdir(config.deposito_ruta):
        click.echo(f'ERROR: En settings.ini no existe deposito_ruta')
        sys.exit(1)


def cargar_inbox(config):
    """ Cargar carpeta inbox del correo electrónico """
    mail = imaplib.IMAP4_SSL(config.servidor_imap)
    mail.login(config.email_direccion, config.email_contrasena)
    mail.list()
    mail.select('inbox') # Accesar la carpeta inbox
    inbox_tipo, inbox_datos = mail.search(None, 'UNSEEN') # Obtener mensajes sin leer
    inbox_ids = inbox_datos[0]
    id_list = inbox_ids.split()
    return(mail, inbox_datos)

def cargar_remitentes(config):
    """ Cargar archivos CSV con datos de los remitentes, entrega un diccionario para consultar con la dirección """
    if config.rama == 'Acuerdos':
        destino_columna = 'Mover Listas de Acuerdos a'
    elif config.rama == 'Sentencias':
        destino_columna = 'Mover Sentencias a'
    else:
        click.echo(f'ERROR: La rama {config.rama} no tiene "columna con ruta" programada.')
        sys.exit(1)
    remitentes = {}
    with open(config.remitentes_csv_ruta) as puntero:
        lector = csv.DictReader(puntero)
        for renglon in lector:
            if renglon['e-mail'] != '' and renglon[destino_columna] != '':
                remitentes[renglon['e-mail']] = {
                    'Distrito': renglon['Distrito'],
                    'Juzgado': renglon['Juzgado'],
                    'Ruta': renglon[destino_columna],
                    }
    return(remitentes)

def enviar_mensaje(config, destinatario_email, asunto, contenido):
    """ Enviar mensaje vía correo electrónico """
    # Armar mensaje
    mensaje = MIMEMultipart()
    mensaje['Subject'] = asunto
    mensaje['From'] = config.email_direccion
    mensaje['To'] = destinatario_email
    mensaje.attach(MIMEText(contenido, 'html'))
    # Enviar mensaje
    try:
        server = smtplib.SMTP(config.servidor_smtp, '587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(config.email_direccion, config.email_contrasena)
        server.sendmail(config.email_direccion, destinatario_email, mensaje.as_string())
    except Exception as e:
        click.echo('AVISO: Fallo en el envío de mensaje por correo electrónico.')
    finally:
        server.quit()

def obtener_ano_mes_directorios():
    """ Entrega el año y mes presente como textos para crear subdirectorios """
    hoy = date.today()
    ano = str(hoy.year)
    meses = { 1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre' }
    mes = meses[hoy.month]
    return(ano, mes)


@cli.command()
@pass_config
def informar(config):
    """ Informar con una línea breve en pantalla """
    click.echo('Voy a informar...')
    tabla = [['e-mail', 'Mover a']]
    remitentes = cargar_remitentes(config)
    for email, informacion in remitentes.items():
        tabla.append([email, informacion['Ruta']])
    if config.notificar:
        # Notificar vía correo electrónico
        asunto = 'Clasificador mandó un informe del ' + str(date.today())
        contenido = tabulate(tabla, headers='firstrow', tablefmt='html')
        enviar_mensaje(config, config.notificar, asunto, contenido)
    else:
        click.echo(tabulate(tabla, headers='firstrow'))


@cli.command()
@pass_config
def leer(config):
    """ Leer """
    click.echo('Voy a leer...')
    salida = []
    mail, inbox_datos = cargar_inbox(config)
    for item in inbox_datos[0].split(): # Recorre los mensajes sin leer
        mensaje_tipo, mensaje_datos = mail.fetch(item, '(RFC822)' )
        mensaje_crudo = mensaje_datos[0][1]
        mensaje_texto = mensaje_crudo.decode('utf-8')
        mensaje = email.message_from_string(mensaje_texto)
        # Separar datos del remitente
        remitente_nombre, remitente_direccion = email.utils.parseaddr(mensaje['from'])
        # Mostrar
        salida.append(f'To:      {mensaje["To"]}')
        salida.append(f'From:    {remitente_direccion}')
        salida.append(f'Subject: {mensaje["Subject"]}')
        salida.append(f'Date:    {mensaje["Date"]}')
        salida.append()
    if config.notificar:
        # Notificar vía correo electrónico
        enviar_mensaje(config, config.notificar, 'Clasificador ha leído los mensajes', '<br>'.join(salida))
    else:
        click.echo('\n'.join(salida))


@cli.command()
@pass_config
def leer_clasificar(config):
    """ Leer y clasificar """
    click.echo('Voy a leer y clasificar...')
    salida = []
    remitentes = cargar_remitentes(config)
    mail, inbox_datos = cargar_inbox(config)
    for item in inbox_datos[0].split(): # Recorre los mensajes sin leer
        mensaje_tipo, mensaje_datos = mail.fetch(item, '(RFC822)' )
        mensaje_crudo = mensaje_datos[0][1]
        mensaje_texto = mensaje_crudo.decode('utf-8')
        mensaje = email.message_from_string(mensaje_texto)
        # Separar datos del remitente
        remitente_nombre, remitente_direccion = email.utils.parseaddr(mensaje['from'])
        # Determinar la ruta de destino a donde depositar los archivos adjuntos
        if remitente_direccion in remitentes:
            remitente = remitentes[remitente_direccion]
            destino_ruta = config.deposito_ruta + '/' + remitente['Ruta']
        else:
            click.echo(salida.append(f'AVISO: Se omite mensaje de {remitente_direccion} porque no hay ruta de destino'))
            continue
        # Validar que exista el subdirectorio
        if not os.path.exists(destino_ruta) or not os.path.isdir(destino_ruta):
            click.echo(salida.append(f'AVISO: Se omite mensaje de {remitente_direccion} porque no existe {destino_ruta}'))
            continue
        # Si no existen, se crean los subdirectorios del año y mes presente
        ano, mes = obtener_ano_mes_directorios()
        destino_ruta = destino_ruta + '/' + str(ano)
        if not os.path.exists(destino_ruta):
            os.mkdir(destino_ruta)
        destino_ruta = destino_ruta + '/' + mes
        if not os.path.exists(destino_ruta):
            os.mkdir(destino_ruta)
        # Bucle para las partes en el mensaje
        adjuntos_guardados = []
        for parte in mensaje.walk():
            nombre = parte.get_filename()
            # Si es un archivo adjunto y termina con pdf
            if bool(nombre) and nombre.endswith('.pdf'):
                # Guardar archivo adjunto
                archivo_ruta = os.path.join(destino_ruta, nombre)
                with open(archivo_ruta, 'wb') as puntero:
                    puntero.write(parte.get_payload(decode=True))
                click.echo(salida.append(f'Se guardó {archivo_ruta}'))
                adjuntos_guardados.append(archivo_ruta)
        # Si no se adjuntaron PDFs
        if len(adjuntos_guardados) == 0:
            click.echo(salida.append(f'AVISO: El mensaje de {remitente_direccion} no tiene archivos PDF'))
    if config.notificar:
        # Notificar vía correo electrónico
        enviar_mensaje(config, config.notificar, 'Clasificador ha leído y clasificado los mensajes', '<br>'.join(salida))


@cli.command()
@pass_config
def leer_clasificar_responder(config):
    """ Leer, clasificar y responder """
    click.echo('Voy a leer, clasificar y responder...')
    salida = []
    remitentes = cargar_remitentes(config)
    mail, inbox_datos = cargar_inbox(config)
    for item in inbox_datos[0].split(): # Recorre los mensajes sin leer
        mensaje_tipo, mensaje_datos = mail.fetch(item, '(RFC822)' )
        mensaje_crudo = mensaje_datos[0][1]
        mensaje_texto = mensaje_crudo.decode('utf-8')
        mensaje = email.message_from_string(mensaje_texto)
        # Separar datos del remitente
        remitente_nombre, remitente_direccion = email.utils.parseaddr(mensaje['from'])
        # Determinar la ruta de destino a donde depositar los archivos adjuntos
        if remitente_direccion in remitentes:
            remitente = remitentes[remitente_direccion]
            destino_ruta = config.deposito_ruta + '/' + remitente['Ruta']
        else:
            click.echo(salida.append(f'AVISO: Se omite mensaje de {remitente_direccion} porque no hay ruta de destino'))
            continue
        # Validar que exista el subdirectorio
        if not os.path.exists(destino_ruta) or not os.path.isdir(destino_ruta):
            click.echo(salida.append(f'AVISO: Se omite mensaje de {remitente_direccion} porque no existe {destino_ruta}'))
            continue
        # Si no existen, se crean los subdirectorios del año y mes presente
        ano, mes = obtener_ano_mes_directorios()
        destino_ruta = destino_ruta + '/' + str(ano)
        if not os.path.exists(destino_ruta):
            os.mkdir(destino_ruta)
        destino_ruta = destino_ruta + '/' + mes
        if not os.path.exists(destino_ruta):
            os.mkdir(destino_ruta)
        # Bucle para las partes en el mensaje
        adjuntos_guardados = []
        for parte in mensaje.walk():
            nombre = parte.get_filename()
            # Si es un archivo adjunto y termina con pdf
            if bool(nombre) and nombre.endswith('.pdf'):
                # Guardar archivo adjunto
                archivo_ruta = os.path.join(destino_ruta, nombre)
                with open(archivo_ruta, 'wb') as puntero:
                    puntero.write(parte.get_payload(decode=True))
                click.echo(salida.append(f'Se guardó {archivo_ruta}'))
                adjuntos_guardados.append(archivo_ruta)
        # Si no se adjuntaron PDFs
        if len(adjuntos_guardados) == 0:
            click.echo(salida.append(f'AVISO: El mensaje de {remitente_direccion} no tiene archivos PDF'))
        else:
            # Responder con Constancia de Publicación
            ahora = datetime.now()
            codigo_html = []
            codigo_html.append('<h1>Poder Judicial<h1>')
            codigo_html.append('<h3>DEL ESTADO DE COAHUILA DE ZARAGOZA</h3>')
            codigo_html.append('<h2>CONSTANCIA DE PUBLICACION</h2>')
            codigo_html.append('<p></p>')
            codigo_html.append('<p>Número DI-{:02d}{:02d}{:02d}{:02d}/{:04d}</p>'.format(ahora.month, ahora.day, ahora.hour, ahora.minute, ahora.year)
            codigo_html.append('<p></p>')
            codigo_html.append('<p>{}</p>'.format(remitente['Juzgado']))
            codigo_html.append('<p>{}</p>'.format(remitente['Distrito']))
            codigo_html.append('<p></p>')
            codigo_html.append('<p>P R E S E N T E</p>')
            codigo_html.append('<p></p>')
            codigo_html.append('<p>Se hace constar que el sistema del portal de Internet del Poder Judicial de Coahuila de Zaragoza, a las {:02d}:{:02d} horas, de {:02d} de {} {} se difundió el/los documento(s) con los siguientes datos:</p>'.format(ahora.hour, ahora.minute, ahora.day, mes, ano))
            codigo_html.append('<p></p>')
            codigo_html.append('<ul>')
            for archivo_ruta in adjuntos_guardados:
                codigo_html.append('<li>{}<li>'.format(os.path.basename(archivo_ruta)))
            codigo_html.append('</ul>')
            codigo_html.append('<p></p>')
            codigo_html.append('<p>Lo anterior para los efectos legales que haya lugar.</p>')
            codigo_html.append('<p></p>')
            codigo_html.append('<p>ATENTAMENTE</p>')
            codigo_html.append('<p>SALTILLO, COAHUILA DE ZARAGOZA, A {:02d} DE {} DE {}</p>'.format(ahora.day, mes.upper(), ano))
            codigo_html.append('<p>DIRECCIÓN DE INFORMÁTICA</p>')
            codigo_html.append('<p></p>')
            enviar_mensaje(config, remitente_direccion, 'Constancia de Publicación', '\n'.join(codigo_html))
    if config.notificar:
        # Notificar vía correo electrónico
        enviar_mensaje(config, config.notificar, 'Clasificador ha leído, clasificado y respondido los mensajes', '<br>'.join(salida))


cli.add_command(informar)
cli.add_command(leer)
cli.add_command(leer_clasificar)
cli.add_command(leer_clasificar_responder)
