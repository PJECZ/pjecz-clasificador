import click
import sys
from datetime import datetime
from comunes.config import pass_config
from buzones.buzon import Buzon
from clientes.clientes import Clientes


@click.group()
@click.option('--fecha', default='', type=str, help='Fecha AAAA-MM-DD')
@click.option('--rama', default='', type=str, help='Acuerdos, Edictos, EdictosJuzgados o Sentencias')
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
    if config.rama not in ('Acuerdos', 'Edictos', 'Edictosjuzgados', 'Sentencias'):
        click.echo('ERROR: Rama no programada.')
        sys.exit(1)
    # Configuración
    try:
        config.cargar_configuraciones()
    except Exception:
        click.echo('ERROR: Falta configuración en settings.ini')
        sys.exit(1)


@cli.command()
@pass_config
def informar(config):
    """ Informar con una línea breve en pantalla """
    click.echo('Voy a informar...')
    click.echo(f'Rama:     {config.rama}')
    click.echo(f'Fecha:    {config.fecha}')
    click.echo(f'e-mail:   {config.email_direccion}')
    click.echo(f'Depósito: {config.deposito_ruta}')
    clientes = Clientes(config)
    clientes.alimentar()
    click.echo(repr(clientes))
    click.echo(clientes.crear_tabla())
    sys.exit(0)


@cli.command()
@pass_config
def leer(config):
    """ Leer """
    click.echo('Voy a leer...')
    buzon = Buzon(config)
    buzon.leer_mensajes()
    click.echo(repr(buzon))
    sys.exit(0)


@cli.command()
@pass_config
def leer_clasificar(config):
    """ Leer y clasificar """
    click.echo('Voy a leer y clasificar...')
    clientes = Clientes(config)
    remitentes = clientes.alimentar()
    buzon = Buzon(config)
    buzon.leer_mensajes()
    buzon.guardar_adjuntos(remitentes)
    click.echo(repr(buzon))
    sys.exit(0)


@cli.command()
@pass_config
def leer_clasificar_responder(config):
    """ Leer, clasificar y responder """
    click.echo('Voy a leer, clasificar y responder...')
    clientes = Clientes(config)
    remitentes = clientes.alimentar()
    buzon = Buzon(config)
    buzon.leer_mensajes()
    buzon.guardar_adjuntos(remitentes)
    buzon.responder_con_acuses()
    click.echo(repr(buzon))
    sys.exit(0)


cli.add_command(informar)
cli.add_command(leer)
cli.add_command(leer_clasificar)
cli.add_command(leer_clasificar_responder)
