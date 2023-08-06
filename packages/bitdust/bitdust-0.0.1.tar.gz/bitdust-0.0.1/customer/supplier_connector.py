#!/usr/bin/env python
# supplier_connector.py
#
# Copyright (C) 2008-2016 Veselin Penev, http://bitdust.io
#
# This file (supplier_connector.py) is part of BitDust Software.
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


"""
.. module:: supplier.

.. role:: red

BitDust supplier_connector() Automat

.. raw:: html

    <a href="supplier.png" target="_blank">
    <img src="supplier.png" style="max-width:100%;">
    </a>

EVENTS:
    * :red:`ack`
    * :red:`close`
    * :red:`connect`
    * :red:`disconnect`
    * :red:`fail`
    * :red:`shutdown`
    * :red:`timer-10sec`
    * :red:`timer-20sec`
"""

#------------------------------------------------------------------------------

_Debug = False
_DebugLevel = 8

#------------------------------------------------------------------------------

import os
import math

#------------------------------------------------------------------------------

from logs import lg

from automats import automat

from system import bpio

from main import settings

from lib import nameurl
from lib import diskspace

from p2p import commands

from p2p import p2p_service

from userid import my_id

#------------------------------------------------------------------------------

_SuppliersConnectors = {}

#------------------------------------------------------------------------------


def connectors():
    """
    """
    global _SuppliersConnectors
    return _SuppliersConnectors


def create(supplier_idurl):
    """
    """
    assert supplier_idurl not in connectors()
    connectors()[supplier_idurl] = SupplierConnector(supplier_idurl)
    return connectors()[supplier_idurl]


def by_idurl(idurl):
    """
    """
    return connectors().get(idurl, None)

#------------------------------------------------------------------------------


class SupplierConnector(automat.Automat):
    """
    This class implements all the functionality of the ``supplier_connector()``
    state machine.
    """

    timers = {
        'timer-10sec': (10.0, ['REFUSE']),
        'timer-20sec': (20.0, ['REQUEST']),
    }

    def __init__(self, idurl):
        """
        """
        self.idurl = idurl
        name = 'supplier_%s' % nameurl.GetName(self.idurl)
        self.request_packet_id = None
        self.callbacks = {}
        try:
            st = bpio.ReadTextFile(settings.SupplierServiceFilename(self.idurl)).strip()
        except:
            st = 'DISCONNECTED'
        if st == 'CONNECTED':
            automat.Automat.__init__(self, name, 'CONNECTED', _DebugLevel, _Debug)
        elif st == 'NO_SERVICE':
            automat.Automat.__init__(self, name, 'NO_SERVICE', _DebugLevel, _Debug)
        else:
            automat.Automat.__init__(self, name, 'DISCONNECTED', _DebugLevel, _Debug)
        for cb in self.callbacks.values():
            cb(self.idurl, self.state, self.state)

    def init(self):
        """
        Method to initialize additional variables and flags at creation of the
        state machine.
        """

    def state_changed(self, oldstate, newstate, event, arg):
        """
        This method intended to catch the moment when automat's state were
        changed.
        """
        if newstate in ['CONNECTED', 'DISCONNECTED', 'NO_SERVICE']:
            supplierPath = settings.SupplierPath(self.idurl, customer_idurl=my_id.getLocalID())
            if not os.path.isdir(supplierPath):
                try:
                    os.makedirs(supplierPath)
                except:
                    lg.exc()
                    return
            bpio.WriteFile(
                settings.SupplierServiceFilename(self.idurl, customer_idurl=my_id.getLocalID(), ),
                newstate,
            )

    def set_callback(self, name, cb):
        self.callbacks[name] = cb

    def remove_callback(self, name):
        if name in self.callbacks.keys():
            self.callbacks.pop(name)

    def A(self, event, arg):
        #---NO_SERVICE---
        if self.state == 'NO_SERVICE':
            if event == 'connect':
                self.state = 'REQUEST'
                self.doRequestService(arg)
                self.GoDisconnect = False
            elif event == 'ack' and self.isServiceAccepted(arg):
                self.state = 'CONNECTED'
                self.doReportConnect(arg)
            elif event == 'shutdown':
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'disconnect':
                self.doReportNoService(arg)
        #---CONNECTED---
        elif self.state == 'CONNECTED':
            if event == 'close':
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'disconnect':
                self.state = 'REFUSE'
                self.doCancelService(arg)
            elif event == 'fail' or event == 'connect':
                self.state = 'REQUEST'
                self.doRequestService(arg)
                self.GoDisconnect = False
        #---CLOSED---
        elif self.state == 'CLOSED':
            pass
        #---DISCONNECTED---
        elif self.state == 'DISCONNECTED':
            if event == 'ack' and self.isServiceAccepted(arg):
                self.state = 'CONNECTED'
                self.doReportConnect(arg)
            elif event == 'shutdown':
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif event == 'disconnect':
                self.state = 'REFUSE'
                self.doCancelService(arg)
            elif event == 'connect':
                self.state = 'REQUEST'
                self.doRequestService(arg)
                self.GoDisconnect = False
            elif event == 'fail':
                self.state = 'NO_SERVICE'
                self.doReportNoService(arg)
        #---REQUEST---
        elif self.state == 'REQUEST':
            if event == 'disconnect':
                self.GoDisconnect = True
            elif event == 'shutdown':
                self.state = 'CLOSED'
                self.doDestroyMe(arg)
            elif self.GoDisconnect and event == 'ack' and self.isServiceAccepted(arg):
                self.state = 'REFUSE'
                self.doCancelService(arg)
            elif event == 'timer-20sec':
                self.state = 'DISCONNECTED'
                self.doCleanRequest(arg)
                self.doReportDisconnect(arg)
            elif event == 'fail' or (event == 'ack' and not self.isServiceAccepted(arg) and not self.GoDisconnect):
                self.state = 'NO_SERVICE'
                self.doReportNoService(arg)
            elif event == 'ack' and not self.GoDisconnect and self.isServiceAccepted(arg):
                self.state = 'CONNECTED'
                self.doReportConnect(arg)
        #---REFUSE---
        elif self.state == 'REFUSE':
            if event == 'shutdown':
                self.state = 'CLOSED'
                self.doCleanRequest(arg)
                self.doDestroyMe(arg)
            elif event == 'timer-10sec' or event == 'fail' or (event == 'ack' and self.isServiceCancelled(arg)):
                self.state = 'NO_SERVICE'
                self.doCleanRequest(arg)
                self.doReportNoService(arg)

    def isServiceAccepted(self, arg):
        """
        Condition method.
        """
        newpacket = arg
        if newpacket.Payload.startswith('accepted'):
            if _Debug:
                lg.out(6, 'supplier_connector.isServiceAccepted !!!! supplier %s connected' % self.idurl)
            return True
        return False

    def isServiceCancelled(self, arg):
        """
        Condition method.
        """
        newpacket = arg
        if newpacket.Command == commands.Ack():
            if newpacket.Payload.startswith('accepted'):
                if _Debug:
                    lg.out(6, 'supplier_connector.isServiceCancelled !!!! supplier %s disconnected' % self.idurl)
                return True
        return False

    def doRequestService(self, arg):
        """
        Action method.
        """
        bytes_needed = diskspace.GetBytesFromString(settings.getNeededString(), 0)
        num_suppliers = settings.getSuppliersNumberDesired()
        if num_suppliers > 0:
            bytes_per_supplier = int(math.ceil(2.0 * bytes_needed / float(num_suppliers)))
        else:
            bytes_per_supplier = int(math.ceil(2.0 * settings.MinimumNeededBytes() / float(settings.DefaultDesiredSuppliers())))
        service_info = 'service_supplier %d' % bytes_per_supplier
        request = p2p_service.SendRequestService(self.idurl, service_info, callbacks={
            commands.Ack(): self._supplier_acked,
            commands.Fail(): self._supplier_failed,
        })
        self.request_packet_id = request.PacketID

    def doCancelService(self, arg):
        """
        Action method.
        """
        request = p2p_service.SendCancelService(
            self.idurl, 'service_supplier',
            callbacks={
                commands.Ack(): self._supplier_acked,
                commands.Fail(): self._supplier_failed})
        self.request_packet_id = request.PacketID

    def doDestroyMe(self, arg):
        """
        Action method.
        """
        connectors().pop(self.idurl)
        self.destroy()

    def doCleanRequest(self, arg):
        """
        Action method.
        """
        # callback.remove_interest(misc.getLocalID(), self.request_packet_id)

    def doReportConnect(self, arg):
        """
        Action method.
        """
        if _Debug:
            lg.out(14, 'supplier_connector.doReportConnect')
        for cb in self.callbacks.values():
            cb(self.idurl, 'CONNECTED')

    def doReportNoService(self, arg):
        """
        Action method.
        """
        if _Debug:
            lg.out(14, 'supplier_connector.doReportNoService')
        for cb in self.callbacks.values():
            cb(self.idurl, 'NO_SERVICE')

    def doReportDisconnect(self, arg):
        """
        Action method.
        """
        if _Debug:
            lg.out(_DebugLevel, 'supplier_connector.doReportDisconnect')
        for cb in self.callbacks.values():
            cb(self.idurl, 'DISCONNECTED')

    def _supplier_acked(self, response, info):
        if _Debug:
            lg.out(16, 'supplier_connector._supplier_acked %r %r' % (response, info))
        self.automat(response.Command.lower(), response)

    def _supplier_failed(self, response, info):
        if _Debug:
            lg.out(16, 'supplier_connector._supplier_failed %r %r' % (response, info))
        self.automat(response.Command.lower(), response)
