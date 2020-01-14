"""
作者         xupeng
邮箱         874582705@qq.com
github主页   https://github.com/xupeng1206

"""

import click


class AppGroup(click.Group):
    pass


cli = AppGroup()


@click.command('create_project', short_help="Create a example web app!")
@click.argument('name', default='example')
def create_project(name):
    click.echo(f'create_project {name}')


cli.add_command(create_project)
