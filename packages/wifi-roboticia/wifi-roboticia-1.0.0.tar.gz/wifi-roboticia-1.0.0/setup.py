#!/usr/bin/env python
from setuptools import setup
import os
import sys

__doc__ = """
Command line tool and library wrappers around iwlist and
/etc/network/interfaces.
"""


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'setuptools',
    'pbkdf2',
]
try:
    import argparse
except:
    install_requires.append('argparse')

version = '1.0.0'

should_install_cli = os.environ.get('WIFI_INSTALL_CLI') not in ['False', '0']
command_name = os.environ.get('WIFI_CLI_NAME', 'wifi')

if command_name == 'wifi.py':
    print(
        "Having a command name of wifi.py will result in a weird ImportError"
        " that doesn't seem possible to work around. Pretty much any other"
        " name seems to work though."
    )
    sys.exit(1)

entry_points = {}
data_files = []

if should_install_cli:
    entry_points['console_scripts'] = [
        '{command} = wifi.cli:main'.format(command=command_name),
    ]
    # make sure we actually have write access to the target folder and if not don't
    # include it in data_files
    if os.access('/etc/bash_completion.d/', os.W_OK):
        data_files.append(('/etc/bash_completion.d/', ['extras/wifi-completion.bash']))
    else:
        print("Not installing bash completion because of lack of permissions.")

setup(
    name='wifi-roboticia',
    version=version,
    author='Rocky Meza, Gavin Wahl, Julien JEHL',
    author_email='contact@roboticia.com',
    description="wifi library using python",
    long_description='Wifi management by command line using python',
    packages=['wifi'],
    entry_points=entry_points,
    test_suite='tests',
    platforms=["Debian"],
    license='BSD',
    install_requires=install_requires,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Topic :: System :: Networking",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
    ],
    data_files=data_files
)
