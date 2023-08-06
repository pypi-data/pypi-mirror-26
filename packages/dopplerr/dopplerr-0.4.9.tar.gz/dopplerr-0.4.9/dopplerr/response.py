# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from enum import Enum

log = logging.getLogger(__name__)


class RequestStatus(Enum):
    UNHANDLED = 1
    PROCESSING = 2
    SUCCESSFUL = 3
    FAILED = -1


class Response(object):
    def __init__(self):
        self.res = {}
        self.__update_status(RequestStatus.UNHANDLED)

    def processing(self, message=None):
        self.__update_status(RequestStatus.PROCESSING, message=message)

    def failed(self, message):
        log.error(message)
        self.__update_status(RequestStatus.FAILED, message=message.lower())

    def unhandled(self, message):
        log.info("Filtered out event: %s", message)
        self.res.setdefault("result", {})["status"] = RequestStatus.UNHANDLED
        self.res.setdefault("result", {})["message"] = message.lower()

    @property
    def is_unhandled(self):
        return self.res.get("result", {}).get("status") == RequestStatus.UNHANDLED

    def __update_status(self, status, message=None):
        self.res.setdefault("result", {})['status'] = status
        if message is not None:
            self.res['result']["message"] = message
        elif "message" in self.res:
            del self.res['result']["message"]

    @property
    def successful(self, message=None):
        return self.__update_status(RequestStatus.SUCCESSFUL, message=message)

    def to_dict(self):
        return self.res

    @property
    def request_type(self):
        return self.res.get("request", {}).get("type", None)

    @request_type.setter
    def request_type(self, thetype):
        self.res.setdefault("request", {})["type"] = thetype

    @property
    def request_event(self):
        return self.res.get("request", {}).get("event", None)

    @request_event.setter
    def request_event(self, event):
        self.res.setdefault("request", {})["event"] = event

    @property
    def exception(self):
        return self.res.get("result", {}).get("exception", None)

    @exception.setter
    def exception(self, exception):
        self.res.setdefault("result", {})["exception"] = exception


class UnhandledResponse(Response):
    def __init__(self, message, *args, **kwargs):
        super(UnhandledResponse, self).__init__(*args, **kwargs)
        self.request_type = "sonarr"
        self.request_type = "unhandled"
        self.failed(message)
