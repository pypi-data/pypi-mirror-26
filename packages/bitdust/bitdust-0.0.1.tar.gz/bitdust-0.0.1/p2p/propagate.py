#!/usr/bin/python
# propagate.py
#
# Copyright (C) 2008-2016 Veselin Penev, http://bitdust.io
#
# This file (propagate.py) is part of BitDust Software.
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
.. module:: propagate.

.. role:: red

When a user starts up he needs to run the stun.py to check what his IP is,
and if it has changed he needs to generate a new identity and send it to
his identity server and all of his contacts.

We also just request new copies of all identities from their servers when
we start up. This is simple and effective.

We should try contacting each contact every hour and if we have not been
able to contact them in 2 or 3 hours then fetch copy of identity from
their server.
"""

#------------------------------------------------------------------------------

_Debug = True
_DebugLevel = 8

#------------------------------------------------------------------------------


import os
import sys
import time

try:
    from twisted.internet import reactor
except:
    sys.exit('Error initializing twisted.internet.reactor in propagate.py')

from twisted.internet.defer import DeferredList, Deferred, TimeoutError

#------------------------------------------------------------------------------

from logs import lg

from system import bpio

from lib import nameurl

from contacts import contactsdb
from contacts import identitycache

from userid import known_servers
from userid import my_id

from p2p import commands

from main import settings

from system import tmpfile

from crypt import signed

from transport import gateway
from transport import stats
from transport import packet_out

from dht import dht_service

#------------------------------------------------------------------------------

_SlowSendIsWorking = False

#------------------------------------------------------------------------------


def init():
    """
    Need to call that at start up to link with transport_control.
    """
    lg.out(4, "propagate.init ")
    # callback.add_finish_file_sending_callback(OnFileSent)


def shutdown():
    """
    
    """
    lg.out(4, "propagate.shutdown")

#------------------------------------------------------------------------------


def propagate(selected_contacts, AckHandler=None, wide=False):
    """
    Run the "propagate" process.

    First need to fetch ``selected_contacts`` IDs from id server. And
    then send our Identity file to that contacts.
    """
    lg.out(6, "propagate.propagate to %d contacts" % len(selected_contacts))
    d = Deferred()

    def contacts_fetched(x):
        lg.out(6, "propagate.propagate.contacts_fetched")
        SendToIDs(selected_contacts, AckHandler, wide)
        d.callback(list(selected_contacts))
        return x
    fetch(selected_contacts).addBoth(contacts_fetched)
    return d


def fetch(list_ids):
    """
    Request a list of identity files.
    """
    lg.out(6, "propagate.fetch identities for %d users" % len(list_ids))
    dl = []
    for url in list_ids:
        if url:
            if not identitycache.FromCache(url):
                dl.append(identitycache.scheduleForCaching(url))
    return DeferredList(dl, consumeErrors=True)


def start(AckHandler=None, wide=False):
    """
    Call ``propagate()`` for all known contacts.
    """
    lg.out(6, 'propagate.start')
    return propagate(contactsdb.contacts_remote(), AckHandler, wide)


def suppliers(AckHandler=None, wide=False, customer_idurl=None):
    """
    Call ``propagate()`` for all suppliers.
    """
    lg.out(6, 'propagate.suppliers')
    return propagate(contactsdb.suppliers(customer_idurl=customer_idurl), AckHandler, wide)


def customers(AckHandler=None, wide=False):
    """
    Call ``propagate()`` for all known customers.
    """
    lg.out(6, 'propagate.customers')
    return propagate(contactsdb.customers(), AckHandler, wide)


def allcontacts(AckHandler=None, wide=False):
    """
    Call ``propagate()`` for all contacts and correspondents, almost the same
    to ``start()``.
    """
    lg.out(6, 'propagate.allcontacts')
    return propagate(contactsdb.contacts_full(), AckHandler, wide)


def single(idurl, ack_handler=None, wide=False, fail_handler=None):
    """
    Do "propagate" for a single contact.
    """
    d = FetchSingle(idurl)
    d.addCallback(lambda x: SendToIDs([idurl, ], ack_handler, wide))
    if ack_handler:
        d.addErrback(fail_handler or ack_handler)
    return d


def update():
    """
    A wrapper of ``SendServers()`` method.
    """
    lg.out(6, "propagate.update")
    return SendServers()


def write_to_dht():
    """

    """
    lg.out(6, "propagate.write_to_dht")
    LocalIdentity = my_id.getLocalIdentity()
    return dht_service.set_value(
        LocalIdentity.getIDURL(),
        LocalIdentity.serialize(),
        age=int(time.time()),
    )

#------------------------------------------------------------------------------


def FetchSingle(idurl):
    """
    Fetch single identity file from given ``idurl``.
    """
    lg.out(6, "propagate.fetch_single " + idurl)
    return identitycache.scheduleForCaching(idurl)


def Fetch(idslist):
    """
    Just a wrapper for ``fetch()`` method.
    """
    return fetch(idslist)


def FetchSuppliers(customer_idurl=None):
    """
    Fetch identity files of all supplier.
    """
    return fetch(contactsdb.suppliers(customer_idurl=customer_idurl))


def FetchCustomers():
    """
    Fetch identity files of all customers.
    """
    return fetch(contactsdb.customers())

#------------------------------------------------------------------------------


def SendServers():
    """
    My identity file can be stored in different locations, see the "sources"
    field.

    So I can use different identity servers to store more secure. This
    method will send my identity file to all my identity servers via
    transport_tcp.
    """
    from transport.tcp import tcp_node
    sendfile, sendfilename = tmpfile.make("propagate")
    os.close(sendfile)
    LocalIdentity = my_id.getLocalIdentity()
    bpio.WriteFile(sendfilename, LocalIdentity.serialize())
    dlist = []
    for idurl in LocalIdentity.sources:
        # sources for out identity are servers we need to send to
        protocol, host, port, filename = nameurl.UrlParse(idurl)
        # if host == settings.IdentityServerName():
        #     host = '67.207.147.183'
        webport, tcpport = known_servers.by_host().get(host,
                                                       (settings.IdentityWebPort(), settings.IdentityServerPort()))
        srvhost = '%s:%d' % (host, int(tcpport))
        dlist.append(tcp_node.send(sendfilename, (host, int(tcpport)), 'Identity', True))
        # dlist.append(gateway.send_file_single('tcp', srvhost, sendfilename, 'Identity'))
    dl = DeferredList(dlist, consumeErrors=True)
    return dl


def SendSuppliers(customer_idurl=None):
    """
    Send my identity file to all my suppliers, calls to ``SendToIDs()`` method.
    """
    lg.out(6, "propagate.SendSuppliers")
    SendToIDs(contactsdb.suppliers(customer_idurl=customer_idurl), HandleSuppliersAck)


def SendCustomers():
    """
    Calls ``SendToIDs()`` to send identity to all my customers.
    """
    lg.out(8, "propagate.SendCustomers")
    SendToIDs(contactsdb.customers(), HandleCustomersAck)


def SlowSendSuppliers(delay=1, customer_idurl=None):
    """
    Doing same thing, but puts delays before sending to every next supplier.

    This is used when need to "ping" suppliers.
    """
    global _SlowSendIsWorking
    if _SlowSendIsWorking:
        lg.out(8, "propagate.SlowSendSuppliers  is working at the moment. skip.")
        return
    lg.out(8, "propagate.SlowSendSuppliers delay=%s" % str(delay))

    def _send(index, payload, delay):
        global _SlowSendIsWorking
        idurl = contactsdb.supplier(index, customer_idurl=customer_idurl)
        if not idurl:
            _SlowSendIsWorking = False
            return
        # transport_control.ClearAliveTime(idurl)
        SendToID(idurl, Payload=payload, wide=True)
        reactor.callLater(delay, _send, index + 1, payload, delay)

    _SlowSendIsWorking = True
    payload = my_id.getLocalIdentity().serialize()
    _send(0, payload, delay)


def SlowSendCustomers(delay=1):
    """
    Same, "slowly" send my identity file to all my customers.
    """

    global _SlowSendIsWorking
    if _SlowSendIsWorking:
        lg.out(8, "propagate.SlowSendCustomers  slow send is working at the moment. skip.")
        return
    lg.out(8, "propagate.SlowSendCustomers delay=%s" % str(delay))

    def _send(index, payload, delay):
        global _SlowSendIsWorking
        idurl = contactsdb.customer(index)
        if not idurl:
            _SlowSendIsWorking = False
            return
        # transport_control.ClearAliveTime(idurl)
        SendToID(idurl, Payload=payload, wide=True)
        reactor.callLater(delay, _send, index + 1, payload, delay)

    _SlowSendIsWorking = True
    payload = my_id.getLocalIdentity().serialize()
    _send(0, payload, delay)


def HandleSuppliersAck(ackpacket, info):
    """
    Called when supplier is "Acked" to my after call to ``SendSuppliers()``.
    """
    lg.out(8, "propagate.HandleSupplierAck %s" % ackpacket.OwnerID)


def HandleCustomersAck(ackpacket, info):
    """
    Called when supplier is "Acked" to my after call to ``SendCustomers()``.
    """
    lg.out(8, "propagate.HandleCustomerAck %s" % ackpacket.OwnerID)


def HandleAck(ackpacket, info):
    lg.out(16, "propagate.HandleAck %r %r" % (ackpacket, info))


def OnFileSent(pkt_out, item, status, size, error_message):
    """
    """
    return False


def SendToID(idurl, ack_handler=None, Payload=None, NeedAck=False, wide=False):
    """
    Create ``packet`` with my Identity file and calls
    ``transport.gateway.outbox()`` to send it.
    """
    lg.out(8, "propagate.SendToID [%s] wide=%s" % (nameurl.GetName(idurl), str(wide)))
    if ack_handler is None:
        ack_handler = HandleAck
    thePayload = Payload
    if thePayload is None:
        thePayload = my_id.getLocalIdentity().serialize()
    p = signed.Packet(
        commands.Identity(),
        my_id.getLocalID(),  # MyID,
        my_id.getLocalID(),  # MyID,
        'Identity',  # my_id.getLocalID(), #PacketID,
        thePayload,
        idurl)
    # callback.register_interest(AckHandler, p.RemoteID, p.PacketID)
    gateway.outbox(p, wide, callbacks={
        commands.Ack(): ack_handler,
        commands.Fail(): ack_handler,
    })
    if wide:
        # this is a ping packet - need to clear old info
        stats.ErasePeerProtosStates(idurl)
        stats.EraseMyProtosStates(idurl)


def SendToIDs(idlist, ack_handler=None, wide=False, NeedAck=False):
    """
    Same, but send to many IDs and also check previous packets to not re-send.
    """
    lg.out(8, "propagate.SendToIDs to %d users, wide=%s" % (len(idlist), wide))
    if ack_handler is None:
        ack_handler = HandleAck
    # MyID = my_id.getLocalID()
    # PacketID = MyID
    LocalIdentity = my_id.getLocalIdentity()
    Payload = LocalIdentity.serialize()
    # Hash = key.Hash(Payload)
    alreadysent = set()
    inqueue = {}
    found_previous_packets = 0
    for pkt_out in packet_out.queue():
        if pkt_out.remote_idurl in idlist:
            if pkt_out.description.count('Identity'):
                if pkt_out.remote_idurl not in inqueue:
                    inqueue[pkt_out.remote_idurl] = 0
                inqueue[pkt_out.remote_idurl] += 1
                found_previous_packets += 1
    for contact in idlist:
        if not contact:
            continue
        if contact in alreadysent:
            # just want to send once even if both customer and supplier
            continue
        if contact in inqueue and inqueue[contact] > 2:
            # now only 2 protocols is working: tcp and udp
            lg.out(8, '        skip sending to %s' % contact)
            continue
#        found_previous_packets = 0
#        for transfer_id in gate.transfers_out_by_idurl().get(contact, []):
#            ti = gate.transfers_out().get(transfer_id, None)
#            if ti and ti.description.count('Identity'):
#                found_previous_packets += 1
#                break
#        if found_previous_packets >= 3:
#            lg.out(8, '        skip sending to %s' % contact)
#            continue
        p = signed.Packet(
            commands.Identity(),
            my_id.getLocalID(),  # MyID,
            my_id.getLocalID(),  # MyID,
            'Identity',  # my_id.getLocalID(), #PacketID,
            Payload,
            contact)
        lg.out(8, "        sending [Identity] to %s" % nameurl.GetName(contact))
        # callback.register_interest(AckHandler, signed.RemoteID, signed.PacketID)
        gateway.outbox(p, wide, callbacks={
            commands.Ack(): ack_handler,
            commands.Fail(): ack_handler, })
        if wide:
            # this is a ping packet - need to clear old info
            stats.ErasePeerProtosStates(contact)
            stats.EraseMyProtosStates(contact)
        alreadysent.add(contact)
    del alreadysent


def PingContact(idurl, timeout=30):
    """
    Called from outside when need to "ping" some user, this will just send my
    Identity to that guy, he will need to respond.

    Previously it request his identity from ID server.
    """
    if _Debug:
        lg.out(_DebugLevel, "propagate.PingContact [%s]" % idurl)
    ping_result = Deferred()

    def _cancel_ack_timeout(x, tmcall):
        lg.out(_DebugLevel, "propagate.PingContact._cancel_ack_timeout")
        if tmcall.active():
            tmcall.cancel()
        return x

    def _ack_handler(response, info, tmcall, res):
        lg.out(_DebugLevel, "propagate.PingContact._ack_handler %s" % str((response, info)))
        if tmcall:
            _cancel_ack_timeout((response, info), tmcall)
        if not res.called:
            res.callback((response, info))

    def _ack_timed_out(tm, cache_request):
        lg.out(_DebugLevel, "propagate.PingContact._ack_timed_out")
        if not cache_request.called:
            cache_request.cancel()
        ping_result.errback(TimeoutError('response was not received within %d seconds' % tm))

    def _identity_cached(x, idsrc, timeout_call, result):
        lg.out(_DebugLevel, "propagate.PingContact._identity_cached %s bytes for [%s]" % (len(idsrc), idurl))
        # TODO Verify()
        SendToIDs(
            idlist=[idurl, ],
            ack_handler=lambda response, info: _ack_handler(response, info, timeout_call, result),
            wide=True,
        )
    idcache_defer = identitycache.scheduleForCaching(idurl, timeout)
    if timeout:
        timeout_call = reactor.callLater(timeout, _ack_timed_out, timeout, idcache_defer)
        idcache_defer.addErrback(_cancel_ack_timeout, timeout_call)
    else:
        timeout_call = None
    idcache_defer.addCallback(_identity_cached, idurl, timeout_call, ping_result)
    idcache_defer.addErrback(ping_result.errback)
    return ping_result
