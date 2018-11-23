# -*- coding: UTF-8 -*-
from {{cookiecutter.project_slug}}.common import patch_io  # noqa
from {{cookiecutter.project_slug}}.common.webeasy import create_app
from {{cookiecutter.project_slug}}.model import database
from . import resource


class ResourceReleaseMiddleware():

    def process_response(self, req, resp, resource, req_succeeded):
        database.close()


app = application = create_app(module=resource,
                               middleware=[ResourceReleaseMiddleware()])
