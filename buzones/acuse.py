import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from funciones.funciones import hoy_dia_mes_ano


class Acuse(object):
    """ Acuse de recepción de un mensaje """

    def __init__(self, config):
        self.config = config
        self.plantillas_env = Environment(
            loader=FileSystemLoader('buzones/plantillas'),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.asunto = ''
        self.contenido = ''

    def elaborar_asunto(self):
        """ Elaborar asunto """
        if self.config.rama == 'Acuerdos':
            self.asunto = 'Acuse de Recepción de Lista de Acuerdos'
        elif self.config.rama == 'Edictos':
            self.asunto = 'Acuse de Recepción de Edicto'
        elif self.config.rama == 'Sentencias':
            self.asunto = 'Acuse de Recepción de Sentencia'
        else:
            raise Exception('ERROR: No está configurada la rama en elaborar_asunto.')
        return(self.asunto)

    def elaborar_contenido(self, identificador, autoridad, distrito, archivos):
        """ Elaborar contenido """
        dia, mes, ano = hoy_dia_mes_ano()
        if self.config.rama == 'Acuerdos':
            plantilla = self.plantillas_env.get_template('listas_de_acuerdos.html.jinja2')
        elif self.config.rama == 'Edictos':
            plantilla = self.plantillas_env.get_template('edictos.html.jinja2')
        elif self.config.rama == 'Sentencias':
            plantilla = self.plantillas_env.get_template('sentencias.html.jinja2')
        else:
            raise Exception('ERROR: No está configurada la rama en elaborar_contenido.')
        self.contenido = plantilla.render(
            identificador=identificador,
            autoridad=autoridad,
            distrito=distrito,
            archivos=archivos,
            dia=dia,
            mes=mes,
            ano=ano,
        )
        return(self.contenido)

    def enviar(self, destinatario_email):
        """ Enviar mensaje vía correo electrónico """
        if self.asunto == '':
            raise Exception('ERROR: No se ha elaborado el asunto del mensaje.')
        if self.contenido == '':
            raise Exception('ERROR: No se ha elaborado el contenido del mensaje.')
        # Armar mensaje
        mensaje = MIMEMultipart()
        mensaje['Subject'] = self.asunto
        mensaje['From'] = self.config.email_direccion
        mensaje['To'] = destinatario_email
        mensaje.attach(MIMEText(self.contenido, 'html'))
        # Enviar mensaje
        try:
            server = smtplib.SMTP(self.config.servidor_smtp, '587')
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.config.email_direccion, self.config.email_contrasena)
            server.sendmail(self.config.email_direccion, destinatario_email, mensaje.as_string())
        except Exception:
            # AVISO: Fallo en el envío de mensaje por correo electrónico.
            pass
        finally:
            server.quit()

    def __repr__(self):
        return('<Acuse>')
