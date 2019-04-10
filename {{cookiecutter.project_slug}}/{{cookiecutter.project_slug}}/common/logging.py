# -*- coding: UTF-8 -*-
import logging

import logzero

_FORMAT = '%(color)s[%(levelname)s] %(message)s%(end_color)s'

LOG = logzero.setup_logger('{{cookiecutter.project_slug}}.application',
                           level=logging.INFO,
                           formatter=logzero.LogFormatter(fmt=_FORMAT))
