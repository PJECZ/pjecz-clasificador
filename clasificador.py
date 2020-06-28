import click
import sys
from comunes.config import pass_config
from comunes.funciones import validar_email, validar_fecha, validar_rama
from buzones.buzon import Buzon
from clientes.clientes import Clientes


@click.group()
@click.option('--email', default='', type=str, help='Correo electrónico (filtro opcional)')
@click.option('--fecha', default='', type=str, help='Fecha AAAA-MM-DD (filtro opcional)')
@click.option('--rama', default='', type=str, help='Acuerdos, Edictos, EdictosJuzgados o Sentencias')
@pass_config
def cli(config, email, fecha, rama):
    """ Validar parámetros y cargar configuraciones """
    click.echo('Hola, ¡soy Clasificador!')
    try:
        config.email = validar_email(email)
        config.fecha = validar_fecha(fecha)
        config.rama = validar_rama(rama)
        config.cargar_configuraciones()
    except Exception as e:
        click.echo(str(e))
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
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
def leer(config):
    """ Leer """
    click.echo('Voy a leer...')
    buzon = Buzon(config)
    try:
        buzon.leer_mensajes()
        click.echo(repr(buzon))
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
def leer_clasificar(config):
    """ Leer y clasificar """
    click.echo('Voy a leer y clasificar...')
    clientes = Clientes(config)
    buzon = Buzon(config)
    try:
        remitentes = clientes.cargar()
        buzon.leer_mensajes()
        buzon.guardar_adjuntos(remitentes)
        click.echo(repr(buzon))
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@pass_config
def leer_clasificar_responder(config):
    """ Leer, clasificar y responder """
    click.echo('Voy a leer, clasificar y responder...')
    clientes = Clientes(config)
    buzon = Buzon(config)
    try:
        remitentes = clientes.cargar()
        buzon.leer_mensajes()
        buzon.guardar_adjuntos(remitentes)
        buzon.responder_con_acuses(remitentes)
        click.echo(repr(buzon))
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    sys.exit(0)


cli.add_command(informar)
cli.add_command(leer)
cli.add_command(leer_clasificar)
cli.add_command(leer_clasificar_responder)
