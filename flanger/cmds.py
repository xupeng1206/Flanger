"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206

"""

import click
import shutil
import os


class AppGroup(click.Group):
    pass


cli = AppGroup()


# 提供穿件实例app的命令
@click.command('create_project', short_help="Create a example web app !")
@click.argument('name', default='example')
def create_project(name):
    click.echo(f'create_project {name} !')
    import flanger
    example_path = flanger.__example__
    if os.path.exists(name):
        click.echo(f'{name} already exists !')
    else:
        shutil.copytree(example_path, name)
        click.echo(f'project {name} created !')


cli.add_command(create_project)
