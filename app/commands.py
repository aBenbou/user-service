import click
from flask.cli import with_appcontext
from app.models.gamification import Badge

@click.command('init-badges')
@with_appcontext
def init_badges():
    """Initialize badges in the database"""
    Badge.create_initial_badges()
    click.echo('Initial badges created successfully') 