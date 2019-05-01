# -*- coding: UTF-8 -*-
from os.path import dirname, join as path_join, realpath
from setuptools import find_packages, setup

from {{cookiecutter.project_slug}}.version import __version__

package = '{{cookiecutter.project_slug}}'
version = __version__


def valid_requirement(line):
    if not line:
        return False
    else:
        ch = line[0]
        return ch not in ('#', '-')


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    root = dirname(realpath(__file__))
    line_iter = (line.strip() for line in open(path_join(root, filename)))
    return [line for line in line_iter if valid_requirement(line)]


setup(
    name=package,
    version=version,
    description='cookiecutter.project_short_description',
    url='',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            '{{cookiecutter.project_name}}-manage = {{cookiecutter.project_slug}}.app.manage:main',
        ],
    },
)
