"""
Install a filter on the logging handler to add some info about requests:
  * client_addr
  * method
  * matched_route
  * path

A pyramid event handler is installed to setup this filter for the current request.
"""
import json
import logging

import cee_syslog_handler
from pyramid.threadlocal import get_current_request

from c2cwsgiutils import _utils, _auth

CONFIG_KEY = 'c2c.log_view_secret'
ENV_KEY = 'LOG_VIEW_SECRET'

LOG = logging.getLogger(__name__)


class _PyramidFilter(logging.Filter):
    """
    A logging filter that adds request information to CEE logs.
    """
    def filter(self, record):
        request = get_current_request()
        if request is not None:
            record.client_addr = request.client_addr
            record.method = request.method
            if request.matched_route is not None:
                record.matched_route = request.matched_route.name
            record.path = request.path
            record.request_id = request.c2c_request_id
        record.level_name = record.levelname
        return True


_PYRAMID_FILTER = _PyramidFilter()


def _un_underscore(message):
    """
    Elasticsearch is not indexing the fields starting with underscore and cee_syslog_handler is starting
    a lot of interesting fields with underscore. Therefore, it's a good idea to remove all those underscore
    prefixes.
    """
    for key, value in list(message.items()):
        if key.startswith('_'):
            new_key = key[1:]
            if new_key not in message:
                del message[key]
                message[new_key] = value
    return message


def _make_message_dict(*args, **kargv):
    """
    patch cee_syslog_handler to rename message->full_message otherwise this part is dropped by syslog.
    """
    msg = cee_syslog_handler.make_message_dict(*args, **kargv)
    if msg['message'] != msg['short_message']:
        # only output full_message if it's different from short message
        msg['full_message'] = msg['message']
    del msg['message']
    return _un_underscore(msg)


class PyramidCeeSysLogHandler(cee_syslog_handler.CeeSysLogHandler):
    """
    A CEE (JSON format) log handler with additional information about the current request.
    """
    def __init__(self, *args, **kargv):
        super().__init__(*args, **kargv)
        self.addFilter(_PYRAMID_FILTER)

    def format(self, record):
        message = _make_message_dict(record, self._debugging_fields, self._extra_fields, False, None,
                                     self._facility)
        return ": @cee: %s" % json.dumps(message)


class JsonLogHandler(logging.StreamHandler):
    """
    Log to stdout in JSON.
    """
    def __init__(self, stream=None):
        super().__init__(stream)
        self.addFilter(_PYRAMID_FILTER)

    def format(self, record):
        message = _make_message_dict(record, debugging_fields=True, extra_fields=True,
                                     fqdn=False, localname=None, facility=None)
        return json.dumps(message)


def install_subscriber(config):
    """
    Install the view to configure the loggers, if configured to do so.
    """
    if _utils.env_or_config(config, ENV_KEY, CONFIG_KEY, False):
        config.add_route("c2c_logging_level", _utils.get_base_path(config) + r"/logging/level",
                         request_method="GET")
        config.add_view(_logging_change_level, route_name="c2c_logging_level", renderer="json", http_cache=0)
        LOG.info("Enabled the /logging/change_level API")


def _logging_change_level(request):
    _auth.auth_view(request, ENV_KEY, CONFIG_KEY)
    name = request.params['name']
    level = request.params.get('level')
    logger = logging.getLogger(name)
    if level is not None:
        LOG.critical("Logging of %s changed from %s to %s", name, logging.getLevelName(logger.level), level)
        logger.setLevel(level)
    return {'status': 200, 'name': name, 'level': logging.getLevelName(logger.level),
            'effective_level': logging.getLevelName(logger.getEffectiveLevel())}
