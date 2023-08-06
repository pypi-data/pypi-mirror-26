#!/usr/bin/python
# tcp_interface.py
#
#
# Copyright (C) 2008-2016 Veselin Penev, http://bitdust.io
#
# This file (tcp_interface.py) is part of BitDust Software.
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
.. module:: tcp_interface.

This is a client side part of the TCP plug-in. The server side part is
placed in the file tcp_process.py.
"""

#------------------------------------------------------------------------------

_Debug = True

#------------------------------------------------------------------------------

import os
import sys

try:
    from twisted.internet import reactor
except:
    sys.exit('Error initializing twisted.internet.reactor in t_tcp.py')

from twisted.web import xmlrpc
from twisted.internet.defer import fail
from twisted.python.failure import Failure

from logs import lg

from main import settings

from lib import misc

from transport.tcp import tcp_node

#------------------------------------------------------------------------------

_GateProxy = None

#------------------------------------------------------------------------------


def proxy():
    global _GateProxy
    return _GateProxy

#------------------------------------------------------------------------------


class GateInterface():

    def init(self, xml_rpc_url_or_object):
        """
        """
        global _GateProxy
        if _Debug:
            lg.out(4, 'tcp_interface.init')
        if isinstance(xml_rpc_url_or_object, str):
            _GateProxy = xmlrpc.Proxy(xml_rpc_url_or_object, allowNone=True)
        else:
            _GateProxy = xml_rpc_url_or_object
        proxy().callRemote('transport_initialized', 'tcp')
        return True

    def shutdown(self):
        """
        """
        if _Debug:
            lg.out(4, 'tcp_interface.shutdown')
        ret = self.disconnect()
        global _GateProxy
        if _GateProxy:
            # del _GateProxy
            _GateProxy = None
        return ret

    def connect(self, options):
        """
        """
        if _Debug:
            lg.out(4, 'tcp_interface.connect %s' % str(options))
        tcp_node.start_streams()
        return tcp_node.receive(options)

    def disconnect(self):
        """
        """
        if _Debug:
            lg.out(4, 'tcp_interface.disconnect')
        tcp_node.stop_streams()
        tcp_node.close_connections()
        return tcp_node.disconnect()

    def build_contacts(self, id_obj):
        """
        """
        result = []
        nowip = misc.readExternalIP()
        result.append('tcp://%s:%s' % (nowip, str(settings.getTCPPort())))
        # TODO:
        #    # if IP is not external and upnp configuration was failed for some reasons
        #    # we may want to use another contact methods, NOT tcp
        #    if IPisLocal() and run_upnpc.last_result('tcp') != 'upnp-done':
        #        lg.out(4, 'p2p_connector.update_identity want to push tcp contact: local IP, no upnp ...')
        #        lid.pushProtoContact('tcp')
        if _Debug:
            lg.out(4, 'tcp_interface.build_contacts : %s' % str(result))
        return result

    def verify_contacts(self, id_obj):
        """
        """
        nowip = misc.readExternalIP()
        tcp_contact = 'tcp://%s:%s' % (nowip, str(settings.getTCPPort()))
        if id_obj.getContactIndex(contact=tcp_contact) < 0:
            if _Debug:
                lg.out(4, 'tcp_interface.verify_contacts returning False: tcp contact not found or changed')
            return False
        if tcp_node.get_internal_port() != settings.getTCPPort():
            if _Debug:
                lg.out(4, 'tcp_interface.verify_contacts returning False: tcp port has been changed')
            return False
        if _Debug:
            lg.out(4, 'tcp_interface.verify_contacts returning True')
        return True

    def send_file(self, remote_idurl, filename, host, description=''):
        """
        """
        host = host.split(':')
        host = (host[0], int(host[1]))
        return tcp_node.send(filename, host, description, False)

    def send_file_single(self, remote_idurl, filename, host, description=''):
        """
        """
        host = host.split(':')
        host = (host[0], int(host[1]))
        return tcp_node.send(filename, host, description, True)

    def connect_to(self, host):
        """
        """
        return tcp_node.connect_to(host)

    def disconnect_from(self, host):
        """
        """
        return tcp_node.disconnect_from(host)

    def cancel_file_sending(self, transferID):
        """
        """
        return tcp_node.cancel_file_sending(transferID)

    def cancel_file_receiving(self, transferID):
        """
        """
        return tcp_node.cancel_file_receiving(transferID)

    def cancel_outbox_file(self, host, filename):
        """
        """
        return tcp_node.cancel_outbox_file(host, filename)

    def list_sessions(self):
        """
        """
        result = []
        for opened_connection in tcp_node.opened_connections().values():
            for channel in opened_connection:
                result.append(channel)
        for started_connection in tcp_node.started_connections():
            result.append(started_connection)
        return result

    def list_streams(self, sorted_by_time=True):
        """
        """
        result = []
        result.extend(tcp_node.list_input_streams(sorted_by_time))
        result.extend(tcp_node.list_output_streams(sorted_by_time))
        return result

#------------------------------------------------------------------------------


def interface_transport_initialized(xmlrpcurl):
    """
    """
    if proxy():
        return proxy().callRemote('transport_initialized', 'tcp', xmlrpcurl)
    lg.warn('transport_tcp is not ready')
    return fail(Failure(Exception('transport_tcp is not ready')))


def interface_receiving_started(host, new_options={}):
    """
    """
    if proxy():
        return proxy().callRemote('receiving_started', 'tcp', host, new_options)
    lg.warn('transport_tcp is not ready')
    return fail(Failure(Exception('transport_tcp is not ready')))


def interface_receiving_failed(error_code=None):
    """
    """
    if proxy():
        return proxy().callRemote('receiving_failed', 'tcp', error_code)
    lg.warn('transport_tcp is not ready')
    return fail(Failure(Exception('transport_tcp is not ready')))


def interface_disconnected(result=None):
    """
    """
    if proxy():
        return proxy().callRemote('disconnected', 'tcp', result)
    lg.warn('transport_tcp is not ready')
    return fail(Failure(Exception('transport_tcp is not ready')))


def interface_register_file_sending(host, receiver_idurl, filename, size=0, description=''):
    """
    """
    if proxy():
        return proxy().callRemote('register_file_sending', 'tcp', '%s:%d' % host, receiver_idurl, filename, size, description)
    lg.warn('transport_tcp is not ready')
    return fail(Failure(Exception('transport_tcp is not ready')))


def interface_register_file_receiving(host, sender_idurl, filename, size=0):
    """
    """
    if proxy():
        return proxy().callRemote('register_file_receiving', 'tcp', '%s:%d' % host, sender_idurl, filename, size)
    lg.warn('transport_tcp is not ready')
    return fail(Failure(Exception('transport_tcp is not ready')))


def interface_unregister_file_sending(transfer_id, status, size=0, error_message=None):
    """
    """
    if proxy():
        return proxy().callRemote('unregister_file_sending', transfer_id, status, size, error_message)
    lg.warn('transport_tcp is not ready')
    return fail(Failure(Exception('transport_tcp is not ready')))


def interface_unregister_file_receiving(transfer_id, status, size=0, error_message=None):
    """
    """
    if proxy():
        return proxy().callRemote('unregister_file_receiving', transfer_id, status, size, error_message)
    lg.warn('transport_tcp is not ready')
    return fail(Failure(Exception('transport_tcp is not ready')))


def interface_cancelled_file_sending(host, filename, size=0, description=None, error_message=None):
    """
    """
    if proxy():
        return proxy().callRemote('cancelled_file_sending', 'tcp', '%s:%d' % host, filename, size, description, error_message)
    lg.warn('transport_tcp is not ready')
    return fail(Failure(Exception('transport_tcp is not ready')))
