# -*- coding: UTF-8 -*-
from datetime import datetime
from peewee import AutoField, DateTimeField
from peewee import Model as PeeweeModel
from playhouse.db_url import connect as db_connect

import logging
import os

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
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
