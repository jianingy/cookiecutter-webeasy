# -*- coding: UTF-8 -*-
from falcon import testing
from pike.discovery import py as discovery

import peewee
import pytest


@pytest.fixture()
def client():
    from {{cookiecutter.project_slug}}.mega_api.wsgi import app
    return testing.TestClient(app)


@pytest.fixture()
def db():
    from {{cookiecutter.project_slug}}.model import database
    from {{cookiecutter.project_slug}} import model as db_model

    def _filter(x):
        return all([
            issubclass(x, peewee.Model),
            hasattr(x, '_meta'),
            not x.__name__.startswith('_'),
        ])

    models = list(filter(_filter, discovery.classes_in_module(db_model)))
    database.drop_tables(models)
    database.create_tables(models)
