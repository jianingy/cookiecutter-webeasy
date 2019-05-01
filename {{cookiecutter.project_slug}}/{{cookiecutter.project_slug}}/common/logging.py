# -*- coding: UTF-8 -*-
import logging
import os

import logzero


_LOG_LEVEL = logging.DEBUG if os.environ.get('DEBUG', False) else logging.INFO
LOG = logzero.setup_logger('interceptron.application', level=_LOG_LEVEL)
