#!/usr/bin/env python

import json
import logging
import sys

import requests

from setup import __VERSION__

objecttype_mapping = {
    'userGroups': ['ug', 'usergroup'],
    'sqlViews': ['sqlview'],
    'constants': ['constant'],
    'optionSets': ['os'],
    'optionGroups': ['optiongroup'],
    'optionGroupSets': ['optiongroupset'],
    'legendSets': ['legendset'],
    'organisationUnitGroups': ['oug', 'orgunitgroups', 'ougroups', 'orgunitgroup', 'ougroup'],
    'organisationUnitGroupSets': ['ougs', 'orgunitgroupsets', 'ougroupsets', 'orgunitgroupset', 'ougroupset'],
    'categoryOptions': ['catoptions', 'catoption', 'categoryoption'],
    'categoryOptionGroups': ['catoptiongroups', 'catoptiongroup', 'categoryoptiongroup'],
    'categoryOptionGroupSets': ['catoptiongroupsets', 'catoptiongroupset', 'categoryoptiongroupset'],
    'categories': ['cat', 'category'],
    'categoryCombos': ['catcombos', 'catcombo', 'categorycombo', 'categorycombination', 'categorycombinations'],
    'dataElements': ['de', 'des', 'dataelement'],
    'dataElementGroups': ['deg', 'degroups', 'degroup', 'dataelementgroup'],
    'dataElementGroupSets': ['degs', 'degroupsets', 'degroupset', 'dataelementgroupset'],
    'indicators': ['i', 'ind', 'indicator'],
    'indicatorGroups': ['ig', 'indgroups', 'indicatorgroup'],
    'indicatorGroupSets': ['igs', 'indgroupsets', 'indicatorgroupset'],
    'dataSets': ['ds', 'dataset'],
    'dataApprovalLevels': ['datasetapprovallevel'],
    'validationRuleGroups': ['validationrulegroup'],
    'interpretations': ['interpretation'],
    'trackedEntityAttributes': ['trackedentityattribute', 'tea', 'teas'],
    'programs': ['program'],
    'eventCharts': ['eventchart'],
    'eventReports': ['eventtables', 'eventreport'],
    'programIndicators': ['pi', 'programindicator'],
    'maps': ['map'],
    'documents': ['document'],
    'reports': ['report'],
    'charts': ['chart'],
    'reportTables': ['reporttable'],
    'dashboards': ['dashboard']
}

# reverse object types so each abbreviation matches to the real valid object in DHIS2
object_types = {}
for key, value in objecttype_mapping.items():
    for acronym in value:
        object_types[acronym] = key

class Dhis(object):
    """Core class for accessing DHIS2 web API"""

    public_access = {
        'none': '--------',
        'readonly': 'r-------',
        'readwrite': 'rw------'
    }

    def get_object_type(self, passed_name):
        real = object_types.get(passed_name.lower(), None)
        if real is not None:
            return real
        else:
            self.log.info('Could not find a valid object type for -f="{}"'.format(passed_name))
            sys.exit()

    def __init__(self, server, username, password, api_version, debug_flag):
        if not server.startswith('https://'):
            self.server = "https://" + server
        else:
            self.server = server
        self.auth = (username, password)
        self.api_version = api_version
        self.log = Logger(debug_flag)

        self.log.info("dhis2-pocket-knife v{}\n".format(__VERSION__))

    def get(self, endpoint, params):
        if self.api_version:
            url = "{}/api/{}/{}.json".format(self.server, self.api_version, endpoint)
        else:
            url = "{}/api/{}.json".format(self.server, endpoint)

        self.log.debug("{} - parameters: {}".format(url, json.dumps(params)))

        try:
            req = requests.get(url, params=params, auth=self.auth)
        except requests.RequestException as e:
            self.log.info(e)
            sys.exit("Error: Check dhis2-pk.log or use debug argument -d")

        self.log.debug(req.url)

        if req.status_code == 200:
            self.log.debug(req.text)
            return req.json()
        else:
            self.log.info(req.text)
            sys.exit("Error: Check dhis2-pk.log or use debug argument -d")

    def post(self, endpoint, params, payload):
        if self.api_version:
            url = "{}/api/{}/{}".format(self.server, self.api_version, endpoint)
        else:
            url = "{}/api/{}".format(self.server, endpoint)

        self.log.debug("{} - parameters: {} \n payload: {}".format(url, json.dumps(params), json.dumps(payload)))

        try:
            req = requests.post(url, params=params, json=payload, auth=self.auth)
        except requests.RequestException as e:
            self.log.info(e)
            sys.exit("Error: Check dhis2-pk.log or use debug argument -d")

        self.log.debug(req.url)

        if req.status_code != 200:
            msg = "[{}] {}".format(str(req.status_code), req.url)
            self.log.info(msg)
            self.log.debug(req.text)
            sys.exit()

    def delete(self, endpoint, uid):
        if self.api_version:
            url = "{}/api/{}/{}/{}".format(self.server, self.api_version, endpoint, uid)
        else:
            url = "{}/api/{}/{}".format(self.server, endpoint, uid)
        try:
            req = requests.delete(url, auth=self.auth)
        except requests.RequestException as e:
            self.log.info(e)
            sys.exit("Error: Check dhis2-pk.log or use debug argument -d")

        msg = "[{}] {}".format(str(req.status_code), req.url)
        self.log.info(msg)
        if req.status_code != 200 or req.status_code != 204:
            self.log.info(req.text)
            sys.exit()


class Logger(object):
    """Core class for Logging to file"""

    def __init__(self, debug_flag):
        format = '%(levelname)s:%(asctime)s %(message)s'
        datefmt = '%Y-%m-%d-%H:%M:%S'
        filename = 'dhis2-pk.log'
        self.debug_flag = debug_flag

        # only log 'requests' library's warning messages (including errors)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        if self.debug_flag:
            logging.basicConfig(filename=filename, level=logging.DEBUG, format=format,
                                datefmt=datefmt)
        else:
            logging.basicConfig(filename=filename, level=logging.INFO, format=format,
                                datefmt=datefmt)

        logging.info("\n=========== START (v {}) ===========".format(__VERSION__))

    @staticmethod
    def info(text):
        print(text)
        logging.info(text)

    @staticmethod
    def debug(text):
        logging.debug(text)
