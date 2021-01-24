"""
Contestador
"""
import sys
import click

from comunes.config import pass_config
from comunes.funciones import validar_email, validar_fecha, validar_rama
from clientes.clientes import Clientes
from depositos.deposito import Deposito


@click.group()
@click.option('--rama', default='', type=str, help='Acuerdos, Edictos, EdictosJuzgados o Sentencias')
@click.option('--distrito', default='', type=str, help='Filtro por Distrito')
@click.option('--autoridad', default='', type=str, help='Filtro por Autoridad')
@click.option('--fecha', default='', type=str, help='Filtro por Fecha AAAA-MM-DD')
@pass_config
def cli(config, rama, distrito, autoridad, fecha):
    """ Rastrea los depoósitos de archivos y envía acuses de publicación """
    click.echo('Hola, ¡soy Contestador!')
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
    click.echo('Voy a informar...')
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
def rastrear(config):
    """ Rastrear documentos """
    click.echo('Voy a rastrear...')
    deposito = Deposito(config)
    try:
        deposito.rastrear()
        click.echo(repr(deposito))
    except Exception as error:
        click.echo(str(error))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
def rastrear_responder(config):
    """ Rastrear documentos y responder """
    click.echo('Voy a rastrear y responder...')
    clientes = Clientes(config)
    deposito = Deposito(config)
    try:
        clientes.cargar()
        deposito.rastrear()
        deposito.responder_con_acuses(clientes)
        click.echo(repr(deposito))
    except Exception as error:
        click.echo(str(error))
        sys.exit(1)
    sys.exit(0)


cli.add_command(informar)
cli.add_command(rastrear)
cli.add_command(rastrear_responder)
