from fabric.api import *
from fabric.contrib import files, project
from fabric.colors import yellow, green, red
from fabric.utils import abort
import os
import time
import socket
import settings


VENV_ACTIVATE = 'source ~/venv_dj13/bin/activate'

@task
def test():
    """ run test suite """
    with prefix(VENV_ACTIVATE):
        with lcd(settings.SITE_ROOT):
            local("coverage run --source='.' manage.py test --verbosity 2")

@task
def clear_pyc():
    cmd = 'find . -name "*.pyc" -exec rm -rf {} \;'
    with lcd(settings.SITE_ROOT):
        local(cmd)