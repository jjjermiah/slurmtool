import rich_click as click
from rich_click import rich_config

from slurmtools.myqueue.myqueue import main as myqueue_main
from slurmtools.subcommands.jobhist import main as jobhist_main

# @tui()
@click.group(
    help='CLI for managing SLURM jobs.',
)
@click.version_option()
@rich_config(help_config={'style_option': 'bold cyan'})
def cli():
    pass


@cli.command(
    help='a prettier version of squeue',
)
@click.option(
    '--format',
    '-f',
    '_format',
    default='simple',
    show_default=True,
    type=click.Choice(
        ['simple', 'spec', 'debug', 'long', 'json'],
        case_sensitive=False,
    ),
    help='The format to use for the output table.',
)
@click.help_option('-h', '--help')
def myqueue(_format: str):
    myqueue_main(_format)


@cli.command(
    help='Gets history of jobs',
)
@click.help_option('-h', '--help')
@click.option(
    '--starttime',
    '-S',
    type=click.DateTime(formats=['%Y-%m-%d', '%Y-%m-%d-%H:%M:%S', '%m.%d.%Y']),
    help='Date before which jobs were started.',
)
@click.option(
    '--debug',
    '-d',
    is_flag=True,
    help='Print debug information.',
)
@click.option(
    '--state',
    '-s',
    help='State of the jobs to show, can be repeated',
    multiple=True,
    type=click.Choice(
        ['PENDING', 'RUNNING', 'SUSPENDED', 'COMPLETED', 'FAILED', 'CANCELLED'],
        case_sensitive=False,
    ),
    show_default=True,
    required=False,
)
def jobhist(
    starttime: click.DateTime,
    debug: bool,
    state: list | None,
):
    jobhist_main(starttime, debug, state)
