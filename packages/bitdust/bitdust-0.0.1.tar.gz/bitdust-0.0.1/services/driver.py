#!/usr/bin/python
# driver.py
#
#
# Copyright (C) 2008-2016 Veselin Penev, http://bitdust.io
#
# This file (driver.py) is part of BitDust Software.
#
# BitDust is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BitDust Software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BitDust Software.  If not, see <http://www.gnu.org/licenses/>.
#
# Please contact us if you have any questions at bitdust.io@gmail.com
#
#
#
#

"""
..

module:: driver
"""

#------------------------------------------------------------------------------

_Debug = False
_DebugLevel = 8

#------------------------------------------------------------------------------

import os
import sys
import importlib

from twisted.internet.defer import Deferred, DeferredList, succeed

#------------------------------------------------------------------------------

if __name__ == '__main__':
    import os.path as _p
    sys.path.insert(
        0, _p.abspath(
            _p.join(
                _p.dirname(
                    _p.abspath(
                        sys.argv[0])), '..')))

#------------------------------------------------------------------------------

from logs import lg

from system import bpio

from main import config

#------------------------------------------------------------------------------

_Services = {}
_BootUpOrder = []
_EnabledServices = set()
_DisabledServices = set()
_StartingDeferred = None
_StopingDeferred = None

#------------------------------------------------------------------------------


def services():
    """
    """
    global _Services
    return _Services


def enabled_services():
    global _EnabledServices
    return _EnabledServices


def disabled_services():
    global _DisabledServices
    return _DisabledServices


def boot_up_order():
    global _BootUpOrder
    return _BootUpOrder


def is_started(name):
    svc = services().get(name, None)
    if svc is None:
        return False
    return svc.state == 'ON'


def is_exist(name):
    return name in services()


def request(name, request, info):
    svc = services().get(name, None)
    if svc is None:
        raise Exception('service %s not found' % name)
    return svc.request(request, info)


def cancel(name, request, info):
    svc = services().get(name, None)
    if svc is None:
        raise Exception('service %s not found' % name)
    return svc.cancel(request, info)

#------------------------------------------------------------------------------


def init():
    """
    """
    if _Debug:
        lg.out(_DebugLevel - 6, 'driver.init')
    available_services_dir = os.path.join(bpio.getExecutableDir(), 'services')
    loaded = set()
    for filename in os.listdir(available_services_dir):
        if not filename.endswith('.py') and not filename.endswith(
                '.pyo') and not filename.endswith('.pyc'):
            continue
        if not filename.startswith('service_'):
            continue
        name = str(filename[:filename.rfind('.')])
        if name in loaded:
            continue
        if name in disabled_services():
            if _Debug:
                lg.out(_DebugLevel - 4, '%s is hard disabled' % name)
            continue
        try:
            py_mod = importlib.import_module('services.' + name)
        except:
            if _Debug:
                lg.out(
                    _DebugLevel -
                    4,
                    '%s exception during module import' %
                    name)
            lg.exc()
            continue
        try:
            services()[name] = py_mod.create_service()
        except:
            if _Debug:
                lg.out(
                    _DebugLevel -
                    4,
                    '%s exception while creating service instance' %
                    name)
            lg.exc()
            continue
        loaded.add(name)
        if not services()[name].enabled():
            if _Debug:
                lg.out(_DebugLevel - 4, '%s is switched off' % name)
            continue
        enabled_services().add(name)
        if _Debug:
            lg.out(_DebugLevel - 4, '%s initialized' % name)
    build_order()
    config.conf().addCallback('services/', on_service_enabled_disabled)


def shutdown():
    """
    """
    if _Debug:
        lg.out(_DebugLevel - 6, 'driver.shutdown')
    config.conf().removeCallback('services/')
    while len(services()):
        name, svc = services().popitem()
        # print sys.getrefcount(svc)
        if _Debug:
            lg.out(_DebugLevel - 6, '[%s] CLOSING' % name)
        svc.automat('shutdown')
        del svc
        svc = None
        enabled_services().discard(name)


def build_order():
    """
    """
    global _BootUpOrder
    order = list(enabled_services())
    progress = True
    fail = False
    counter = 0
    while progress and not fail:
        progress = False
        counter += 1
        if counter > len(enabled_services()) * len(enabled_services()):
            lg.warn('dependency recursion')
            fail = True
            break
        for position in range(len(order)):
            name = order[position]
            svc = services()[name]
            depend_position_max = -1
            for depend_name in svc.dependent_on():
                if depend_name not in order:
                    fail = True
                    lg.warn('dependency not satisfied: #%d:%s depend on %s' % (
                        position, name, depend_name,))
                    break
                depend_position = order.index(depend_name)
                if depend_position > depend_position_max:
                    depend_position_max = depend_position
            if fail:
                break
            if position < depend_position_max:
                # print name, order[depend_position_max]
                order.insert(depend_position_max + 1, name)
                del order[position]
                progress = True
                break
    _BootUpOrder = order
    return order


def start():
    """
    """
    global _StartingDeferred
    if _StartingDeferred:
        lg.warn('driver.start already called')
        return _StartingDeferred
    if _Debug:
        lg.out(_DebugLevel - 6, 'driver.start')
    dl = []
    for name in boot_up_order():
        svc = services().get(name, None)
        if not svc:
            raise ServiceNotFound(name)
        if not svc.enabled():
            continue
        if svc.state == 'ON':
            continue
        d = Deferred()
        dl.append(d)
        svc.automat('start', d)
    if len(dl) == 0:
        return succeed(1)
    _StartingDeferred = DeferredList(dl)
    _StartingDeferred.addCallback(on_started_all_services)
    return _StartingDeferred


def stop():
    """
    """
    global _StopingDeferred
    if _StopingDeferred:
        lg.warn('driver.stop already called')
        return _StopingDeferred
    if _Debug:
        lg.out(_DebugLevel - 6, 'driver.stop')
    dl = []
    for name in reversed(boot_up_order()):
        svc = services().get(name, None)
        if not svc:
            raise ServiceNotFound(name)
        d = Deferred()
        dl.append(d)
        svc.automat('stop', d)
    _StopingDeferred = DeferredList(dl)
    _StopingDeferred.addCallback(on_stopped_all_services)
    return _StopingDeferred

#------------------------------------------------------------------------------


def on_service_callback(result, service_name):
    """
    
    """
    if _Debug:
        lg.out(_DebugLevel +
               8, 'driver.on_service_callback %s : [%s]' %
               (service_name, result))
    svc = services().get(service_name, None)
    if not svc:
        raise ServiceNotFound(service_name)
    if result == 'started':
        if _Debug:
            lg.out(_DebugLevel - 6, '[%s] STARTED' % service_name)
        relative_services = []
        for other_name in services().keys():
            if other_name == service_name:
                continue
            other_service = services().get(other_name, None)
            if not other_service:
                raise ServiceNotFound(other_name)
            if other_service.state == 'ON':
                continue
            for depend_name in other_service.dependent_on():
                if depend_name == service_name:
                    relative_services.append(other_service)
        if len(relative_services) > 0:
            # global _StartingDeferred
            # if _StartingDeferred:
            for relative_service in relative_services:
                if not relative_service.enabled():
                    continue
                if relative_service.state == 'ON':
                    continue
                relative_service.automat('start')
    elif result == 'stopped':
        if _Debug:
            lg.out(_DebugLevel - 6, '[%s] STOPPED' % service_name)
        for depend_name in svc.dependent_on():
            depend_service = services().get(depend_name, None)
            if not depend_service:
                raise ServiceNotFound(depend_name)
            depend_service.automat('depend-service-stopped')
    return result


def on_started_all_services(results):
    if _Debug:
        lg.out(_DebugLevel - 6, 'driver.on_started_all_services')
    global _StartingDeferred
    _StartingDeferred = None
    return results


def on_stopped_all_services(results):
    if _Debug:
        lg.out(_DebugLevel - 6, 'driver.on_stopped_all_services')
    global _StopingDeferred
    _StopingDeferred = None
    return results


def on_service_enabled_disabled(path, newvalue, oldvalue, result):
    if not result:
        return
    if not path.endswith('/enabled'):
        return
    svc_name = path.replace(
        'services/',
        'service_').replace(
        '/enabled',
        '').replace(
            '-',
        '_')
    svc = services().get(svc_name, None)
    if svc:
        if newvalue == 'true':
            svc.automat('start')
        else:
            svc.automat('stop')
    else:
        lg.warn('%s not found: %s' % (svc_name, path))

#------------------------------------------------------------------------------


class ServiceAlreadyExist(Exception):
    pass


class RequireSubclass(Exception):
    pass


class ServiceNotFound(Exception):
    pass

#------------------------------------------------------------------------------


def main():
    from main import settings
    lg.set_debug_level(20)
    settings.init()
    init()
    # print '\n'.join(_BootUpOrder)
    shutdown()


if __name__ == '__main__':
    main()
