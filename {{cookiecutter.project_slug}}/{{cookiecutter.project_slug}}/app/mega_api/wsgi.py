# -*- coding: UTF-8 -*-
from {{cookiecutter.project_slug}}.common import patch_io
patch_io.patch_all()  # noqa

from {{cookiecutter.project_slug}}.common.webeasy import create_app
from {{cookiecutter.project_slug}}.models import database
from . import views


class ResourceReleaseMiddleware():

    def process_response(self, req, resp, resource, req_succeeded):
        database.close()


app = application = create_app(module=views,
                               middleware=[ResourceReleaseMiddleware()])
