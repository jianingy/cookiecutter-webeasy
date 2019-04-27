# -*- coding: UTF-8 -*-
from marshmallow import Schema
from marshmallow.exceptions import ValidationError

import falcon
import functools
import os
import pike.discovery.py as discovery
import raven
import traceback
import ujson

from {{cookiecutter.project_slug}}.common.exceptions import ClientException
from {{cookiecutter.project_slug}}.common.logging import LOG

RAVEN_CLIENT = raven.Client(os.environ['SENTRY_DSN'])


def _catch_all(error, req, resp, params):
    if not (hasattr(error, 'alert_sentry') and error.alert_sentry):
        data = {
            'request': {
                'url': req.url,
                'method': req.method,
                'query_string': req.query_string,
                'env': req.env,
                'data': req.params,
                'headers': req.headers,
            },
        }
        message = (error.title if isinstance(error, falcon.HTTPError)
                   else str(error))
        RAVEN_CLIENT.captureException(message=message, data=data)
    if isinstance(error, ClientException):
        data = error.data if hasattr(error, 'data') else None
        code = error.error_code if hasattr(error, 'error_code') else -1
        reason = error.message if hasattr(error, 'message') else str(error)
        retval = dict(reason=reason, data=data, code=code)
        raise falcon.HTTPStatus(error.http_status_code,
                                body=ujson.dumps(retval))
    if not isinstance(error, falcon.HTTPError):
        data = error.data if hasattr(error, 'data') else None
        tb = ''.join(traceback.format_tb(error.__traceback__))
        LOG.error('v' * 78)
        LOG.error(f'{error} {type(error)} \n{tb}'.strip())
        LOG.error('^' * 78)
        code = error.error_code if hasattr(error, 'error_code') else -1
        reason = error.message if hasattr(error, 'message') else str(error)
        retval = dict(reason=reason, data=data, code=code)
        if bool(os.environ.get('DEBUG', '')):
            retval['traceback'] = tb
        raise falcon.HTTPStatus(falcon.HTTP_INTERNAL_SERVER_ERROR,
                                body=ujson.dumps(retval))
    else:
        raise error


def _catch_validation(error, req, resp, params):
    body = ujson.dumps(dict(reason='VALIDATION_ERROR',
                            detail=error.args[0],
                            code=1))
    raise falcon.HTTPStatus(falcon.HTTP_BAD_REQUEST, body=body)


def create_app(module, middleware=[]):
    app = falcon.API(middleware=middleware, independent_middleware=True)
    num_routes = 0
    for v in discovery.get_all_classes(module):
        if hasattr(v, 'route') and isinstance(v.route, str):
            LOG.info(f'Adding route {v.route} from {v.__name__} ...')
            app.add_route(v.route, v())
            num_routes += 1
    LOG.info(f'#{num_routes} routes has been successfully added.')

    # add order matters
    app.add_error_handler(Exception, _catch_all)
    app.add_error_handler(ValidationError, _catch_validation)

    return app


def schema(query=None, data=None, reply=None):

    query_schema, data_schema = query, data

    def _urldecode(schema, formdata):
        data = {}
        for key, value in formdata.items():
            if not key.endswith('[]'):
                data[key] = value[-1] if isinstance(value, list) else value
            else:
                data[key] = value
        return schema.load(data).data

    def wrapper(function):

        mimes = {
            'form': 'application/x-www-form-urlencoded',
            'json': 'application/json',
        }

        @functools.wraps(function)
        def f(handler, *args, **kwargs):
            req, resp, *_ = args
            if query_schema and isinstance(query_schema, Schema):
                kwargs.update({'query': _urldecode(query_schema, req.params)})
            content_type = req.content_type or ''
            if data_schema and isinstance(data_schema, Schema):
                body = req.stream.read().decode('UTF-8')
                if content_type.startswith('application/json'):
                    body = body if body else '{}'
                    kwargs.update({'data': data_schema.loads(body).data})
                elif content_type.startswith('application/x-www-form-urlencoded'):
                    params = falcon.uri.parse_query_string(body)
                    kwargs.update({'data': _urldecode(data_schema, params)})
                else:
                    kwargs.update({'data': body})
            elif data_schema:
                body = req.stream.read().decode('UTF-8')
                if content_type.startswith(mimes['form']):
                    kwargs.upate({'data': ujson.loads(body)})
                else:
                    kwargs.update({'data': body})

            retval = function(handler, *args, **kwargs)

            if reply and isinstance(reply, Schema):
                resp.content_type = falcon.MEDIA_JSON
                if isinstance(retval, tuple) and len(retval) > 1:
                    code, data = int(retval[0]), reply.dump(retval[1]).data
                    if len(retval) > 2:
                        resp.status = retval[2]
                else:
                    code, data = 0, reply.dump(retval).data
                resp.body = ujson.dumps(dict(code=code, data=data))
            elif isinstance(retval, dict):
                resp.content_type = falcon.MEDIA_JSON
                resp.body = ujson.dumps(retval)
            else:
                resp.content_type = falcon.MEDIA_TEXT
                resp.body = str(retval)
            return retval

        return f

    return wrapper
