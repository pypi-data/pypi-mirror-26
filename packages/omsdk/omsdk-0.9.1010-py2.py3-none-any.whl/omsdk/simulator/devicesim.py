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
import logging
import os
from omsdk.sdkprotopref import ProtoPreference, ProtocolEnum
from omsdk.sdkcenum import TypeHelper
import re
import json

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

logger = logging.getLogger(__name__)

class Simulation:
    def __init__(self):
        self.record = False
        self.simulate = False
    def start_recording(self):
        self.record = True
        self.simulate = False
    def end_recording(self):
        self.record = False
        self.simulate = False
    def start_simulating(self):
        self.simulate = True
        self.record = False
    def end_simulating(self):
        self.record = False
        self.simulate = False
    def is_recording(self):
        return self.record
    def is_simulating(self):
        return self.simulate

    def simulate_config(self, ipaddr):
        mypath = "."
        for i in ["simulator", ipaddr, 'config']:
            mypath = os.path.join(mypath, i)
        mypath = os.path.join(mypath, "config.xml")
        if os.path.exists(mypath) and not os.path.isdir(mypath):
            return mypath
        return None

    def record_config(self, ipaddr, config, name='config.xml'):
        mypath = "."
        for i in ["simulator", ipaddr, 'config']:
            mypath = os.path.join(mypath, i)
            if not os.path.exists(mypath):
                os.mkdir(mypath)
        mypath = os.path.join(mypath, name)
        with open(mypath, 'w') as myconfig:
                myconfig.write(config)
        return mypath

    def simulate_proto(self, ipaddr, enumid, clsName):
        mypath = "."
        for i in ["simulator", ipaddr, str(enumid)]:
            mypath = os.path.join(mypath, i)
        mypath = os.path.join(mypath, clsName + ".json")
        retval = {'Data' : {}, 'Status' : 'Failed', 'Message' : 'No file found'}
        if os.path.exists(mypath) and not os.path.isdir(mypath):
            with open(mypath) as enum_data:
                retval = json.load(enum_data)
        return retval

    def record_proto(self, ipaddr, enumid, clsName, retval):
        mypath = "."
        for i in ["simulator", ipaddr, str(enumid)]:
            mypath = os.path.join(mypath, i)
            if not os.path.exists(mypath):
                os.mkdir(mypath)
        with open(os.path.join(mypath, clsName + ".json"), "w") as f:
            json.dump(retval, f, sort_keys=True, indent=4, \
                 separators=(',', ': '))

    def simulator_connect(self, ipaddr, enumid, protoobj):
        mypath = "."
        for i in ["simulator", ipaddr, str(enumid)]:
            mypath = os.path.join(mypath, i)
        if os.path.exists(mypath) and os.path.isdir(mypath):
            if enumid != ProtocolEnum.WSMAN:
                return protobj
            sjson = os.path.join(mypath, 'System.json')
            simspec = None
            for i in protoobj.views:
                if TypeHelper.resolve(i) == 'System':
                    simspec = re.sub(".*/", '', protoobj.views[i])
                    break
            if os.path.exists(sjson) and simspec:
                with open(sjson, 'r') as endata:
                    _s = json.load(endata)
                    if _s and 'Data' in _s and \
                       _s['Data'] and simspec in _s['Data']:
                        return protoobj
        return None

Simulator = Simulation()

