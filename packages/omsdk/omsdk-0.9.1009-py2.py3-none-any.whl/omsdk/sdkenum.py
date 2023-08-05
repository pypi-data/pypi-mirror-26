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
from enum import Enum
from omsdk.sdkcenum import EnumWrapper, TypeHelper, PY2Enum

if PY2Enum:
    from enum import EnumValue

import re
import sys
import logging


logger = logging.getLogger(__name__)

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

class AutoNumber(Enum):
    def __new__(cls):
        value = 1 << len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

class Filter(object):
    def check(self, scopeType):
        not_implemented

    def allowedtype(self, scopeType):
        not_implemented

    def add(self,scopeType):
        if self.check(scopeType):
            self.mix = self.mix | TypeHelper.resolve(scopeType)
        else:
            raise AttributeError("Filter can only take Flag in argument")

    def __init__(self, *args):
        self.mix =  0
        for scopeType in args:
            self.add(scopeType)

    def isset(self,scopeType):
        n = TypeHelper.resolve(scopeType)
        return ((self.mix & n)  == n)

    def unset(self,scopeType):
        n = TypeHelper.resolve(scopeType)
        self.mix = (~(self.mix & n)  & self.mix)


    def _all(self, enumtype):
        if self.allowedtype(enumtype):
            for i in enumtype:
                self.add(i)
        else:
            logger.debug(str(enumtype) + " is not allowed for " + str(self))
        return self

    def test(self, enumtype):
        if self.allowedtype(enumtype):
            for i in enumtype:
                logger.debug("  " + str(i) + "=" + str(self.isset(i)))
        else:
            logger.debug(str(enumtype) + " is not allowed for " + str(self))

MonitorScopeMap = {
    "Key"            : 1 << 0,
    "Metrics"        : 1 << 1,
    "ConfigState"    : 1 << 2,
    # Inventory includes all
    "BasicInventory" : 1 << 3,
    "OtherInventory" : 1 << 4,
    "Inventory"      : 1 << 3 | 1 << 4,

    "MainHealth"     : 1 << 10, # Main component health
    "OtherHealth"    : 1 << 11, # other health component
    # Health includes all health
    "Health"         : 1 << 10 | 1 << 11,
}
MonitorScope = EnumWrapper("MS", MonitorScopeMap).enum_type


class MonitorScopeFilter(Filter):
    def __init__(self, *args):
        if PY2:
            super(MonitorScopeFilter, self).__init__(*args)
        else:
            super().__init__(*args)
    def allowedtype(self, scopeType):
        return type(scopeType) == type(MonitorScope)
    def check(self, scopeEnum):
        return TypeHelper.belongs_to(MonitorScope, scopeEnum)
    def all(self):
        return self._all(MonitorScope)

def CreateMonitorScopeFilter(argument = ""):
    if argument == "":
        argument  = "Health+Inventory+Metrics+ConfigState"
    monitorfilter = MonitorScopeFilter()
    for i in argument.split("+"):
        for j in MonitorScope:
            if TypeHelper.get_name(j, MonitorScopeMap) == i:
                monitorfilter.add(j)
    return monitorfilter

MonitorScopeFilter_All = MonitorScopeFilter().all()

class ComponentScope:
    def __init__(self, *args):
        self.comps = {}
        for comp in args:
            try:
                if PY2Enum and isinstance(comp, EnumValue):
                    self.comps[comp.key] = True
                    continue
            except:
                pass

            if isinstance(comp,Enum):
                self.comps[comp.value] = True
            else:
                self.comps[comp] = True

    def isMatch(self, comp):
        return (comp in self.comps)

    def printx(self):
        for i in self.comps:
            print (i)

class RegExpFilter:
    def __init__(self, *args):
        self.rexp = []
        for rexp in args:
            self.rexp.append(re.compile(rexp))

    def isMatch(self, obj):
        for rexp in self.rexp:
            if rexp.match(obj):
                return True
        return False

class DeviceGroupFilter(RegExpFilter):
    pass

class DeviceFilter(RegExpFilter):
    pass

