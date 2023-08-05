#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
import logging

import os
import platform
import re
import subprocess
import sys
from collections import defaultdict
from importlib import import_module

import django
import django.core.management
import requests
from django.core.management.base import CommandError
from django.core.management.color import color_style
from django.conf import settings
import six

import otree
from otree.settings import get_default_settings

# =============================================================================
# CONSTANTS
# =============================================================================

MANAGE_URL = (
    "https://raw.githubusercontent.com/oTree-org/oTree/master/manage.py")


NO_SETTINGS_COMMANDS = [
    'help', 'version', '--help', '--version', '-h',
    'compilemessages', 'makemessages',
    'startapp', 'startproject',
]


OVERRIDE_DJANGO_COMMANDS = ['startapp', 'startproject']


# =============================================================================
# CLASSES
# =============================================================================

class OTreeManagementUtility(django.core.management.ManagementUtility):

    def limit_text(self, helptext, limit=80):
        if len(helptext) <= limit:
            return helptext
        limited = helptext
        while len(limited) > limit - 3:
            limited = " ".join(limited.split()[:-1])
        if limited != helptext:
            limited += "..."
        return limited

    def get_commands(self):
        return django.core.management.get_commands()

    def main_help_text(self, commands_only=False):
        """
        Returns the script's main help text, as a string.
        """
        if commands_only:
            usage = sorted(self.get_commands().keys())
        else:

            second_line = (
                "Type {} help <subcommand>' for help on a specific "
                "subcommand.").format(self.prog_name)
            usage = ["", second_line, "", "Available subcommands:"]

            commands_dict = defaultdict(lambda: [])
            for name, app in six.iteritems(self.get_commands()):
                if app == 'django.core':
                    app = 'django'
                else:
                    app = app.rpartition('.')[-1]
                commands_dict[app].append(name)
            style = color_style()
            for app in sorted(commands_dict.keys()):
                usage.append("")
                usage.append(style.NOTICE("[%s]" % app))
                for name in sorted(commands_dict[app]):
                    helptext = " ".join(
                        self.fetch_command(name).help.splitlines())
                    helptext = self.limit_text(helptext, 80)
                    usage.append("  {} - {}".format(name, helptext))
            # Output an extra note if settings are not properly configured
            if self.settings_exception is not None:
                usage.append(style.NOTICE(
                    "Note that only Django core commands are listed "
                    "as settings are not properly configured (error: %s)."
                    % self.settings_exception))

        return '\n'.join(usage)

    def fetch_command(self, subcommand):
        if subcommand in OVERRIDE_DJANGO_COMMANDS:
            command_module = import_module(
                'otree.management.commands.{}'.format(subcommand))
            return command_module.Command()
        return super(OTreeManagementUtility, self).fetch_command(subcommand)


# =============================================================================
# FUNCTIONS
# =============================================================================

def otree_and_django_version(*args, **kwargs):
    otree_ver = otree.get_version()
    django_ver = django.get_version()
    return "oTree: {} - Django: {}".format(otree_ver, django_ver)


def execute_from_command_line(arguments, script_file):

    try:
        subcommand = arguments[1]
    except IndexError:
        subcommand = 'help'  # default

    # Workaround for Python 2 & windows. For some reason, runserver
    # complains if the script you are using to initialize celery does not end
    # on '.py'. That's why we require a manage.py file to be around.

    # originally this was written for a problem with billiard/celery,
    # but now for runserver.
    # See https://github.com/celery/billiard/issues/129 for more details.
    cond = (
        platform.system() == 'Windows' and
        not script_file.lower().endswith('.py') and
        subcommand not in NO_SETTINGS_COMMANDS
    )

    if cond:

        scriptdir = os.path.dirname(os.path.abspath(script_file))
        managepy = os.path.join(scriptdir, 'manage.py')
        if not os.path.exists(managepy):
            error_lines = []

            error_lines.append(
                "It seems that you do not have a file called 'manage.py' in "
                "your current directory. This is a requirement when using "
                "otree on windows."
            )
            error_lines.append("")
            error_lines.append("")
            error_lines.append(
                "Please download the file {url} and save it as 'manage.py' in "
                "the directory {directory}".format(
                    url=MANAGE_URL, directory=scriptdir))
            raise CommandError("\n".join(error_lines))
        args = [sys.executable] + [managepy] + arguments[1:]
        process = subprocess.Popen(args,
                                   stdin=sys.stdin,
                                   stdout=sys.stdout,
                                   stderr=sys.stderr)
        return_code = process.wait()
        sys.exit(return_code)

    # only monkey patch when is necesary
    if "version" in arguments or "--version" in arguments:
        sys.stdout.write(otree_and_django_version() + '\n')
        try:
            pypi_updates_cli()
        except:
            pass
    else:
        utility = OTreeManagementUtility(arguments)
        utility.execute()


SETTINGS_NOT_FOUND_MESSAGE = (
    "Cannot import otree settings.\n"
    "Please make sure that you are in the root directory of your "
    "oTree project. This directory contains a settings.py "
    "and a manage.py file.")


def otree_cli():
    """
    This function is the entry point for the ``otree`` console script.
    """

    try:
        subcommand = sys.argv[1]
    except IndexError:
        subcommand = 'help'  # default

    # We need to add the current directory to the python path as this is not
    # set by default when no using "python <script>" but a standalone script
    # like ``otree``.
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    argv = sys.argv

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

    # some commands don't need the setings.INSTALLED_APPS
    # see: https://github.com/oTree-org/otree-core/issues/388
    try:
        settings.INSTALLED_APPS
    except ImportError as exc:
        if subcommand in NO_SETTINGS_COMMANDS:
            settings.configure(**get_default_settings({}))
        # need to differentiate between an ImportError because settings.py
        # was not found, vs. ImportError because settings.py imports another
        # module that is not found.
        elif os.path.isfile('settings.py'):
            raise
        else:
            ExceptionClass = type(exc)
            raise ExceptionClass(SETTINGS_NOT_FOUND_MESSAGE)

    execute_from_command_line(argv, 'otree')


def check_pypi_for_updates() -> dict:
    '''return a dict because it needs to be json serialized for the AJAX
    response'''
    # MUST IMPORT HERE, because otree.management.cli is imported before
    # django is loaded
    from otree import common_internal
    if not common_internal.PYPI_CHECK_UPDATES:
        return {}

    logging.getLogger("requests").setLevel(logging.WARNING)

    try:
        response = requests.get(
            'http://pypi.python.org/pypi/otree-core/json',
            timeout=5,
        )
        assert response.ok
        data = json.loads(response.content.decode())
    except:
        # could be requests.exceptions.Timeout
        # or another error (404/500/firewall issue etc)
        return {'pypi_connection_error': True}

    semver_re = re.compile(r'^(\d+)\.(\d+)\.(\d+)$')

    installed_dotted = otree.__version__
    installed_match = semver_re.match(installed_dotted)

    if installed_match:
        # compare to the latest stable release

        installed_tuple = [int(n) for n in installed_match.groups()]

        releases = data['releases']
        newest_tuple = [0, 0, 0]
        newest_dotted = ''
        for release in releases:
            release_match = semver_re.match(release)
            if release_match:
                release_tuple = [int(n) for n in release_match.groups()]
                if release_tuple > newest_tuple:
                    newest_tuple = release_tuple
                    newest_dotted = release
        newest = newest_tuple
        installed = installed_tuple

        update_needed = (newest > installed and (
                newest[0] > installed[0] or newest[1] > installed[1] or
                newest[2] - installed[2] >= 8))

    else:
        # compare to the latest release, whether stable or not
        newest_dotted = data['info']['version'].strip()
        update_needed = newest_dotted != installed_dotted

    if update_needed:
        update_message = (
            'Your otree-core package is out-of-date '
            '(version {}; latest is {}). '
            'You should upgrade with:\n '
            '"pip3 install --upgrade otree-core"\n '
            'and update your requirements_base.txt.'.format(
                installed_dotted, newest_dotted))
    else:
        update_message = ''
    return {
        'pypi_connection_error': False,
        'update_needed': update_needed,
        'installed_version': installed_dotted,
        'newest_version': newest_dotted,
        'update_message': update_message,
    }


def pypi_updates_cli():
    result = check_pypi_for_updates()
    if result['pypi_connection_error']:
        return
    if result['update_needed']:
        print(result['update_message'])
