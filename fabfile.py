import sys

from fabric.api import local, task
from fabric.colors import green, red


DEFAULT_MODE = 'dev'
SERVER_MODES = {
    'dev': 'development',
    'prod': 'production',
    'test': 'test'
}


def success(message):
    print(green(message))


def error(message):
    print(red(message))
    sys.exit()


def get_mode(mode):
    if mode not in SERVER_MODES:
        error('Mode "%s" - does not exist' % mode)
    return SERVER_MODES[mode]


def watch(time, command_name, mode):
    local('watch -n %d ./manage.py %s --settings=settings.%s' % (
        time, command_name, get_mode(mode)
    ))


def django_manage(command):
    local('python manage.py %s' % command)


@task
def smtp():
    success("Run SMTP server at localhost:1025")
    local("python -m smtpd -n -c DebuggingServer localhost:1025")


@task
def reset_db(mode=DEFAULT_MODE):
    local('rm -rf db.sqlite3')
    django_manage('syncdb --noinput')


@task
def run():
    success('Run server')
    django_manage('runserver 0.0.0.0:8000')


@task
def test(module_name):
    success('Test')
    django_manage('test %s' % module_name)


@task
def depending():
    success('Main requirements')
    local('pip install -r requirements.txt')
