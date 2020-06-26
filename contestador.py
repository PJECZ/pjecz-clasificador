import click
import sys
from comunes.config import pass_config
from comunes.funciones import validar_email, validar_fecha, validar_rama
from clientes.clientes import Clientes
from depositos.deposito import Deposito


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
def rastrear(config):
    """ Rastrear documentos en la rama y fecha dada """
    click.echo('Voy a rastrear...')
    deposito = Deposito(config)
    try:
        deposito.rastrear()
        click.echo(repr(deposito))
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)
    sys.exit(0)


@cli.command()
@click.option('--enviar', is_flag=True, help='Enviar mensajes')
@pass_config
def responder(config, enviar):
    """ Responder con un mensaje vía correo electrónico """
    click.echo('Voy a rastrear y responder...')
    clientes = Clientes(config)
    clientes.cargar()
    deposito = Deposito(config)
    deposito.rastrear()
    if deposito.cantidad == 0:
        click.echo(f'AVISO: No se encontraron documentos con fecha {config.fecha}')
        sys.exit(0)
    for documento in deposito.documentos:
        destinatarios = clientes.filtrar_con_archivo_ruta(documento.ruta)
        if len(destinatarios) == 0:
            click.echo(f'AVISO: No hay destinatarios para {documento.ruta}')
        else:
            for email, informacion in destinatarios.items():
                documento.definir_acuse()
                if enviar:
                    documento.enviar_acuse(email)
                else:
                    click.echo(f"- SIMULO envar mensaje a {email} sobre {documento.archivo}")
                    click.echo(documento.acuse.asunto)
                    click.echo(documento.acuse.contenido)
                    click.echo()
    sys.exit(0)


cli.add_command(informar)
cli.add_command(rastrear)
cli.add_command(responder)
