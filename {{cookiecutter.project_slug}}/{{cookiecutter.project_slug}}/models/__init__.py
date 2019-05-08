# -*- coding: UTF-8 -*-
from datetime import datetime
import logging
import os

from peewee import AutoField, DateTimeField, SQL
from peewee import Model as PeeweeModel
from playhouse.db_url import connect as db_connect


database = db_connect(os.environ.get('DATABASE_URL', None))

if bool(os.environ.get('DEBUG', False)):
    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)


class _BaseModel(PeeweeModel):

    class Meta:
        database = database


class _BaseRecordModel(_BaseModel):
    id_ = AutoField(column_name='id', primary_key=True)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

