#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# Copyright � 2017 Dell Inc. or its subsidiaries. All rights reserved.
# Dell, EMC, and other trademarks are trademarks of Dell Inc. or its
# subsidiaries. Other trademarks may be trademarks of their respective owners.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Vaideeswaran Ganesan
#
import sys
import io
import logging
import json
from enum import Enum

import xml.etree.ElementTree as ET

import requests
import requests.adapters
import requests.exceptions
import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from omsdk.sdkprotobase import ProtocolBase
from omsdk.sdkcenum import EnumWrapper, TypeHelper
from omsdk.http.sdkrestpdu import RestRequest, RestResponse
from omsdk.http.sdkhttpep import HttpEndPoint, HttpEndPointOptions

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

ReturnValueMap = {
    'Success' : 0,
    'Error' : 2,
    'JobCreated' : 4096,
    'Invalid' : -1
}

ReturnValue = EnumWrapper('ReturnValue', ReturnValueMap).enum_type


class RestOptions(HttpEndPointOptions):
    def __init__(self):
        if PY2:
            super(RestOptions, self).__init__()
        else:
            super().__init__()

class RestProtocol(ProtocolBase):
    def __init__(self, ipaddr, creds, pOptions):
        if PY2:
            super(RestProtocol, self).__init__()
        else:
            super().__init__()
        headers = { 'Content-Type' : 'application/json' }
        self.proto = HttpEndPoint(ipaddr, creds, pOptions, headers)
        self._logger = logging.getLogger(__name__)

    def identify(self):
        """ Identifies the target product """
        wsm = RestRequest()
        wsm.identify()
        return self._communicate(wsm)

    def enumerate(self, clsName, resource, select = {}, resetTransport = False):
        wsm = RestRequest()
        wsm.enumerate(to = self.proto.endpoint, ruri=resource,
                      selectors = select)
        return self._communicate(wsm)

    def operation(self, wsmancmds, cmdname, *args):
        ruri = wsmancmds[cmdname]["ResourceURI"]
        act = wsmancmds[cmdname]["Action"]
        sset = {}
        tset = wsmancmds[cmdname]["SelectorSet"]
        for i in tset["w:Selector"]:
            sset[i['@Name']]= i['#text']
        toargs = self._build_ops(wsmancmds, cmdname, *args)

        wsm = RestRequest()
        wsm.set_header(self.endpoint, ruri, (ruri + "/" + act))
        wsm.add_selectors(sset)
        wsm.add_body(ruri, act, toargs['retval'])
        return self._communicate(wsm)

    def _communicate(self, wsm, name = None):
        try :
            self.proto.connect()
            self._logger.debug("Sending: " + wsm.get_text())
            result = self.proto.ship_payload(wsm.get_text())
            # Status = 202 - job created successfully
            # Status = 200 - job created successfully
            self._logger.debug("Received: " + str(result))
            en = RestResponse().execute_str(result)
            out = self._parse_output(en, name)
            return out
        except Exception as ex:
            self._logger.debug(str(ex))
            # fake as if the error came from the WSMAN subsystem
            sx = RestRequest()
            sx.add_error(ex)
            self._logger.debug(sx.get_text())
            en = RestResponse().execute_str(sx.get_text())
            out = self._parse_output(en)
            return out

    def printx(self, json_object):
        if json_object is None:
            logger.debug("<empty json>")
            return False
        logger.debug(json.dumps(json_object, sort_keys=True, indent=4, \
              separators=(',', ': ')))

    # retVal['Status'] = Success, Failed, Invalid JSON,
    # retval['Data'][component] = {}
    # retval['Fault.Data']['Reason'] = Reason
    # retval['Fault.Data']['Text'] = Message
    # retval['Message'] = Message
    # retval['Return'] = enum(ReturnValue).value
    # retval['Job']['JobId'] = jobid
    def _parse_output(self, en, name=None):
        retval = {}
        if "Header" in en:
            rgsp = "http://schemas.xmlsoap.org/ws/2004/09/transfer/GetResponse"
            if "Action" in en["Header"] and en["Header"]["Action"] == rgsp:
                retval['Status'] = 'Success'
                retval['Data'] = en['Body']
        if not "Body" in en:
            retval['Status'] = 'Invalid JSON. Does not have Body!'
        elif "ClientFault" in en["Body"]:
            retval['Status'] = 'Found Client (SDK) Side Fault'
            retval['Fault.Data'] = en["Body"]["ClientFault"]
            if "Reason" in en["Body"]["ClientFault"] and \
               "Text" in en["Body"]["ClientFault"]["Reason"]:
                retval['Message'] = RestResponse().get_message(en["Body"]["ClientFault"]["Reason"])
        elif "Fault" in en["Body"]:
            retval['Status'] = 'Found Fault'
            retval['Fault.Data'] = en["Body"]["Fault"]
            if "Detail" in en["Body"]["Fault"]:
                retval['Message'] = RestResponse().get_message(en["Body"]["Fault"]["Reason"])
            if retval['Message'] == "":
                retval['Message'] = RestResponse().get_message(en["Body"]["Fault"]["Detail"])
        elif "EnumerateResponse" in en["Body"]:
            retval['Status'] = 'Success'
            retval['Data'] = en["Body"]["EnumerateResponse"]["Items"]
        elif "IdentifyResponse" in en["Body"]:
            retval['Status'] = 'Success'
            retval['Data'] = en["Body"]
        else:
            for entry in en["Body"]:
                if not entry.endswith("_OUTPUT"):
                    continue
                retval['Data'] = en["Body"]
                retval['Status'] = 'Not understood the message. Sorry!'
                if "Message" in en["Body"][entry]:
                     retval['Status'] = en["Body"][entry]["Message"]
                     retval['Message'] = en["Body"][entry]["Message"]
                if "MessageID" in en["Body"][entry]:
                    retval['MessageID'] = en["Body"][entry]["MessageID"]
                if "ReturnValue" in en["Body"][entry]:
                    ret = int(en["Body"][entry]["ReturnValue"])
                    retval['Return'] = TypeHelper.get_name(ret, ReturnValueMap)
                    retval['Status'] = retval['Return']
                    if ret == TypeHelper.resolve(ReturnValue.JobCreated):
                        retval['Job'] = { "ResourceURI" : "", "JobId" : "" }
                        ss = en["Body"][entry]
                        if "Job" in ss:
                            ss = ss["Job"]
                        if "EndpointReference" in ss:
                            ss = ss["EndpointReference"]
                        if "ReferenceParameters" in ss:
                            ss = ss["ReferenceParameters"]
                        if "ResourceURI" in ss:
                            retval['Job']['ResourceURI'] = ss["ResourceURI"]
                        if "SelectorSet" in ss:
                            ss = ss["SelectorSet"]
                        if "Selector" in ss:
                            ss = ss["Selector"]
                        retval['Job']['JobId'] = ss[0] 
                        retval['Status'] = 'Success'
        if not 'Status' in retval:
            retval['Status'] = 'Dont understand the message'
            retval['Data'] = en["Body"]
        return retval

