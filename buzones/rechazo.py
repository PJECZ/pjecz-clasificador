"""
Buzones, Rechazo
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from comunes.funciones import hoy_dia_mes_ano


class Rechazo:
    """Rechazo de recepción de recepción de documentos"""

    def __init__(self, config):
        """Inicializar"""
        self.config = config
        self.plantillas_env = Environment(
            loader=FileSystemLoader("buzones/plantillas"),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.asunto = None
        self.contenido = None
        self.email = None
        self.ya_enviado = False

    def crear_asunto(self):
        """Elaborar asunto"""
        if self.config.buzones_rechazo_asunto != "":
            self.asunto = self.config.buzones_rechazo_asunto
            return self.asunto
        else:
            raise Exception("ERROR: Falta buzones_rechazo_asunto en settings.ini")

    def crear_contenido(self, causa, autoridad, distrito, archivos):
        """Elaborar contenido"""
        dia, mes, ano = hoy_dia_mes_ano()
        if self.config.buzones_rechazo_contenido != "":
            plantilla = self.plantillas_env.get_template(self.config.buzones_rechazo_contenido)
        else:
            raise Exception("ERROR: Falta buzones_rechazo_contenido en settings.ini")
        self.contenido = plantilla.render(
            causa=causa,
            autoridad=autoridad,
            distrito=distrito,
            archivos=archivos,
            dia=dia,
            mes=mes,
            ano=ano,
        )
        return self.contenido

    def enviar(self, email):
        """Enviar mensaje vía correo electrónico"""
        if self.ya_enviado is False:
            if self.asunto is None:
                raise Exception("ERROR: No se ha elaborado el asunto del mensaje.")
            if self.contenido is None:
                raise Exception("ERROR: No se ha elaborado el contenido del mensaje.")
            # En modo desarrollo se sustituye la dirección de correo electrónico
            if self.config.email_desarrollo != "":
                email = self.config.email_desarrollo
            # Armar mensaje
            mensaje = MIMEMultipart()
            mensaje["Subject"] = self.asunto
            mensaje["From"] = self.config.email_direccion
            mensaje["To"] = email
            mensaje.attach(MIMEText(self.contenido, "html"))
            # Enviar mensaje
            try:
                server = smtplib.SMTP(self.config.servidor_smtp, "587")
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.config.email_direccion, self.config.email_contrasena)
                server.sendmail(self.config.email_direccion, email, mensaje.as_string())
            except Exception:
                raise Exception("AVISO: Fallo en el envío de mensaje por correo electrónico.")
            finally:
                server.quit()
            self.email = email
            self.ya_enviado = True

    def __repr__(self):
        """Representación"""
        if self.ya_enviado:
            return "<Rechazo> Enviado a {}".format(self.email)
        return "<Rechazo>"
