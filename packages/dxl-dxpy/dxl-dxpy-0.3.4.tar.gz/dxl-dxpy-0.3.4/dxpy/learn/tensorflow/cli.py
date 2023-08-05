import click


@click.group()
def tf():
    pass


@tf.command()
@click.option('--config', '-c', type=str, help='configs .yml filename')
def run(config):
    from .service import run
    run(config)
