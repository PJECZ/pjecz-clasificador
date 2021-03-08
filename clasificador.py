"""
Clasificador
"""
import sys
import click

from comunes.config import pass_config
from comunes.funciones import validar_email, validar_fecha, validar_rama
from clientes.clientes import Clientes
from buzones.buzon import Buzon


@click.group()
@click.option("--rama", default="", type=str, help="Acuerdos, Edictos, EdictosJuzgados o Sentencias")
@click.option("--distrito", default="", type=str, help="Filtro por Distrito")
@click.option("--autoridad", default="", type=str, help="Filtro por Autoridad")
@click.option("--fecha", default="", type=str, help="Filtro por Fecha AAAA-MM-DD")
@pass_config
def cli(config, rama, distrito, autoridad, fecha):
    """ Mi objetivo es leer los buzones, clasificar y enviar acuses de los mensajes recibidos """
    click.echo("Hola, ¡soy Clasificador!")
    try:
        config.rama = validar_rama(rama)
        config.distrito = validar_email(distrito)
        config.autoridad = validar_email(autoridad)
        config.fecha = validar_fecha(fecha)
        config.cargar_configuraciones()
    except Exception as error:
        click.echo(str(error))
        sys.exit(1)


@cli.command()
@pass_config
def informar(config):
    """ Informar mostrando los clientes """
    click.echo("Voy a informar...")
    clientes = Clientes(config)
    try:
        clientes.cargar()
        click.echo(repr(clientes))
        click.echo(clientes.crear_tabla())
    except Exception as error:
        click.echo(str(error))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
def leer(config):
    """ Leer """
    click.echo("Voy a leer...")
    buzon = Buzon(config)
    try:
        buzon.leer_mensajes()
        click.echo(repr(buzon))
    except Exception as error:
        click.echo(str(error))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
def leer_clasificar(config):
    """ Leer buzón y clasificar documentos """
    click.echo("Voy a leer y clasificar...")
    clientes = Clientes(config)
    buzon = Buzon(config)
    try:
        remitentes = clientes.cargar()
        buzon.leer_mensajes()
        buzon.guardar_adjuntos(remitentes)
        click.echo(repr(buzon))
    except Exception as error:
        click.echo(str(error))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
def leer_clasificar_responder(config):
    """ Leer buzón, clasificar documentos y responder """
    click.echo("Voy a leer, clasificar y responder...")
    clientes = Clientes(config)
    buzon = Buzon(config)
    try:
        remitentes = clientes.cargar()
        buzon.leer_mensajes()
        buzon.guardar_adjuntos(remitentes)
        buzon.responder_con_acuses(remitentes)
        click.echo(repr(buzon))
    except Exception as error:
        click.echo(str(error))
        sys.exit(1)
    sys.exit(0)


cli.add_command(informar)
cli.add_command(leer)
cli.add_command(leer_clasificar)
cli.add_command(leer_clasificar_responder)
