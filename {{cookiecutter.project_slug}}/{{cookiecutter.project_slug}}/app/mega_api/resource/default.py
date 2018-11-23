# -*- coding: UTF-8 -*-
from {{cookiecutter.project_slug}}.common.webeasy import schema
from {{cookiecutter.project_slug}}.version import __version__


class TableSectionBind:

    route = '/api/v1/version'

    @schema(reply=True)
    def on_get(self, req, resp):
        return dict(version=__version__)
