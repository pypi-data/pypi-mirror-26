#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import os
import sys
from datetime import datetime

import requests

try:
    from .helpers import object_types
except ImportError:
    from src.core.static import object_types

from src.__init__ import ROOT_DIR


def get_pkg_version():
    __version__ = ''
    with open(os.path.join(ROOT_DIR, 'version.py')) as f:
        exec (f.read())
    return __version__


class Dhis(object):
    """Core class for accessing DHIS2 web API"""

    public_access = {
        'none': '--------',
        'readonly': 'r-------',
        'readwrite': 'rw------'
    }

    def __init__(self, server, username, password, api_version):
        if '/api' in server:
            print('Please do not specify /api/ in the server argument: e.g. -s=play.dhis2.org/demo')
            sys.exit()
        if server.startswith('localhost') or server.startswith('127.0.0.1'):
            server = 'http://{}'.format(server)
        elif server.startswith('http://'):
            server = server
        elif not server.startswith('https://'):
            server = 'https://{}'.format(server)
        self.auth = (username, password)
        if api_version:
            self.api_url = '{}/api/{}'.format(server, api_version)
        else:
            self.api_url = '{}/api'.format(server)
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        server_name = server.replace('https://', '').replace('.', '-').replace('/', '-')
        self.file_timestamp = '{}_{}'.format(now, server_name)

    def abort(self, request):
        msg = u"++++++ ERROR ++++++\n+++HTTP code: {}\n+++URL: {}\n+++RESPONSE: {}"
        self.log.info(msg.format(request.status_code, request.url, request.text))
        sys.exit()

    def get_object_type(self, passed_name):
        obj_types = object_types()
        valid_obj_name1 = obj_types.get(passed_name.lower(), None)
        if valid_obj_name1 is None:
            valid_obj_name2 = obj_types.get(passed_name[:-1].lower(), None)
            if valid_obj_name2 is None:
                self.log.info(u"+++ Could not find a valid object type for -t='{}'".format(passed_name))
                sys.exit()
            else:
                return valid_obj_name2
        return valid_obj_name1

    def get(self, endpoint, file_type='json', params=None):
        url = "{}/{}.{}".format(self.api_url, endpoint, file_type)

        self.log.debug(u"GET: {} - parameters: {}".format(url, json.dumps(params)))

        try:
            req = requests.get(url, params=params, auth=self.auth)
        except requests.RequestException as e:
            self.abort(req)

        self.log.debug(u"URL: {}".format(req.url))

        if req.status_code == 200:
                self.log.debug(u"RESPONSE: {}".format(req.text))
                if file_type == 'json':
                    return req.json()
                else:
                    return req.text
        else:
            self.abort(req)

    def post(self, endpoint, params, payload):
        url = "{}/{}".format(self.api_url, endpoint)
        self.log.debug(u"POST: {} \n parameters: {} \n payload: {}".format(url, json.dumps(params), json.dumps(payload)))

        try:
            req = requests.post(url, params=params, json=payload, auth=self.auth)
        except requests.RequestException as e:
            self.abort(req)

        self.log.debug(req.url)

        if req.status_code != 200:
            self.abort(req)


class Logger(object):
    """Core class for Logging to file"""

    def __init__(self, debug_flag):
        logformat = '%(levelname)s:%(asctime)s %(message)s'
        datefmt = '%Y-%m-%d-%H:%M:%S'
        filename = 'dhis2-pk.log'
        self.debug_flag = debug_flag

        # only log 'requests' library's warning messages (including errors)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        if self.debug_flag:
            logging.basicConfig(filename=filename, level=logging.DEBUG, format=logformat,
                                datefmt=datefmt)
        else:
            logging.basicConfig(filename=filename, level=logging.INFO, format=logformat,
                                datefmt=datefmt)

    @staticmethod
    def startinfo(script_path):
        script_name = os.path.splitext(os.path.basename(script_path))[0]
        logging.info(u"\n\n===== dhis2-pocket-knife v{} - {} =====".format(get_pkg_version(), script_name))

    @staticmethod
    def info(text):
        if isinstance(text, Exception):
            logging.debug(repr(text))
        else:
            try:
                print(text)
            except UnicodeDecodeError:
                print(text.encode('utf-8'))
            finally:
                logging.info(text.encode('utf-8'))

    @staticmethod
    def debug(text):
        logging.debug(text.encode('utf-8'))
