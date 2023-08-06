#!/usr/bin/python
# jsonrpc_server.py
#
# Copyright (C) 2008-2016 Veselin Penev, http://bitdust.io
#
# This file (jsonrpc_server.py) is part of BitDust Software.
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

module:: jsonrpc_server
"""

import time
import pprint
import traceback

from twisted.internet import reactor
from twisted.internet.defer import Deferred, succeed
from twisted.web import server

if __name__ == '__main__':
    import sys
    import os.path as _p
    sys.path.insert(0, _p.abspath(_p.join(_p.dirname(_p.abspath(sys.argv[0])), '..')))

from lib.fastjsonrpc.server import JSONRPCServer
from lib.fastjsonrpc.jsonrpc import JSONRPCError

#------------------------------------------------------------------------------

from logs import lg

from interface import api

#------------------------------------------------------------------------------

_JsonRPCServer = None

#------------------------------------------------------------------------------

def init(json_rpc_port=None):
    global _JsonRPCServer
    lg.out(4, 'jsonrpc_server.init')
    if _JsonRPCServer:
        lg.warn('already started')
        return
    from main import settings
    from system import bpio
    if not json_rpc_port:
        json_rpc_port = settings.getJsonRPCServerPort()
    bpio.AtomicWriteFile(settings.LocalJsonRPCPortFilename(), str(json_rpc_port))
    # TODO: add protection: accept connections only from local host: 127.0.0.1
    _JsonRPCServer = reactor.listenTCP(json_rpc_port, server.Site(BitDustJsonRPCServer()))
    lg.out(4, '    started on port %d' % json_rpc_port)


def shutdown():
    global _JsonRPCServer
    lg.out(4, 'jsonrpc_server.shutdown')
    if not _JsonRPCServer:
        return succeed(None)
    result = Deferred()
    lg.out(4, '    calling stopListening()')
    _JsonRPCServer.stopListening().addBoth(lambda *args: result.callback(*args))
    _JsonRPCServer = None
    return result

#------------------------------------------------------------------------------


class BitDustJsonRPCServer(JSONRPCServer):

    def _register_execution(self, request_dict, result):
        if result is None:
            result = dict()
        result['execution'] = '%3.6f' % (time.time() - request_dict['_executed'])
        lg.out(4, "jsonrpc_server._register_execution : %s sec. ,  started at %d" % (result['execution'], request_dict['_executed']))
        return result

    def _convert_filemanager_response(self, result):
        if 'status' not in result:
            result['status'] = 'OK'
        if 'result' in result and isinstance(result['result'], dict):
            if 'success' in result['result'] and not result['result']['success']:
                result['status'] = 'ERROR'
                result['errors'] = [result['result']['error'], ]
                del result['result']
            else:
                result['result'] = [result['result'], ]
        return result

    def _catch_filemanager_methods(self, request_dict):
        if not request_dict['method'].startswith('filemanager_'):
            return None
        try:
            fm_method = request_dict['method'].replace('filemanager_', '')
            fm_request = {}
            params = [] if 'params' not in request_dict else request_dict['params']
            fm_request['params'] = {
                i[0]: i[1] for i in map(lambda p: p.split("=", 1), params)}
            fm_request['params']['mode'] = fm_method
            request_dict = {'_executed': time.time(), }
        except Exception as exc:
            lg.exc()
            return api.ERROR(exc.message)
        try:
            fm_result = api.filemanager(fm_request)
            if isinstance(fm_result, Deferred):
                fm_result.addCallback(self._convert_filemanager_response)
            else:
                fm_result = self._convert_filemanager_response(fm_result)
        except Exception as exc:
            lg.exc()
            fm_result = api.ERROR(exc.message)
        return fm_result

    def _callMethod(self, request_dict):
        lg.out(12, 'jsonrpc_server._callMethod:\n%s' % pprint.pformat(request_dict))
        request_dict['_executed'] = time.time()
        try:
            fm_result = self._catch_filemanager_methods(request_dict)
            if fm_result is None:
                result = JSONRPCServer._callMethod(self, request_dict)
            else:
                result = fm_result
        except JSONRPCError as exc:
            lg.err(exc.strerror)
            result = api.ERROR(exc.strerror)
        except Exception as exc:
            lg.exc()
            result = api.ERROR(str(traceback.format_exc()), message=exc.message)
        if isinstance(result, Deferred):
            result.addCallback(
                lambda result: self._register_execution(request_dict, result))
        else:
            result = self._register_execution(request_dict, result)
        return result

    def jsonrpc_stop(self):
        return api.stop()

    def jsonrpc_restart(self, show=False):
        return api.restart(show)

    def jsonrpc_show(self):
        return api.show()

    def jsonrpc_filemanager(self, json_request):
        return api.filemanager(json_request)

    def jsonrpc_config_list(self, sort=False):
        return api.config_list(sort)

    def jsonrpc_config_get(self, key):
        return api.config_get(key)

    def jsonrpc_config_set(self, key, value):
        return api.config_set(key, value)

    def jsonrpc_key_get(self, key_id, include_private=False):
        return api.key_get(key_id, include_private=include_private)

    def jsonrpc_keys_list(self, sort=False, include_private=False):
        return api.keys_list(sort, include_private=include_private)

    def jsonrpc_key_create(self, key_alias, key_size=4096):
        return api.key_create(key_alias, key_size)

    def jsonrpc_key_erase(self, key_id):
        return api.key_erase(key_id)

    def jsonrpc_key_share(self, key_id, idurl):
        return api.key_share(key_id, idurl)

    def jsonrpc_files_list(self, remote_path=None):
        return api.files_list(remote_path=remote_path)

    def jsonrpc_files_sync(self):
        return api.files_sync()

    def jsonrpc_file_info(self, remote_path):
        return api.file_info(remote_path)

    def jsonrpc_file_create(self, remote_path, as_folder=False):
        return api.file_create(remote_path, as_folder=as_folder)

    def jsonrpc_file_delete(self, remote_path):
        return api.file_delete(remote_path)

    def jsonrpc_files_downloads(self):
        return api.files_downloads()

    def jsonrpc_file_download_start(self, remote_path, destination_path=None):
        return api.file_download_start(remote_path, destination_path=destination_path)

    def jsonrpc_file_download_stop(self, remote_path):
        return api.file_download_stop(remote_path)

    def jsonrpc_files_uploads(self, include_running=True, include_pending=True):
        return api.files_uploads(include_running=include_running, include_pending=include_pending)

    def jsonrpc_file_upload_start(self, local_path, remote_path, wait_result=True):
        return api.file_upload_start(local_path, remote_path, wait_result=wait_result)

    def jsonrpc_file_upload_stop(self, remote_path):
        return api.file_upload_stop(remote_path)

    def jsonrpc_suppliers_list(self):
        return api.suppliers_list()

    def jsonrpc_supplier_replace(self, index_or_idurl):
        return api.supplier_replace(index_or_idurl)

    def jsonrpc_supplier_change(self, index_or_idurl, new_idurl):
        return api.supplier_change(index_or_idurl, new_idurl)

    def jsonrpc_suppliers_ping(self):
        return api.suppliers_ping()

    def jsonrpc_customers_list(self):
        return api.customers_list()

    def jsonrpc_customer_reject(self, idurl):
        return api.customer_reject(idurl)

    def jsonrpc_customers_ping(self):
        return api.customers_ping()

    def jsonrpc_space_donated(self):
        return api.space_donated()

    def jsonrpc_space_consumed(self):
        return api.space_consumed()

    def jsonrpc_space_local(self):
        return api.space_local()

    def jsonrpc_automats_list(self):
        return api.automats_list()

    def jsonrpc_services_list(self):
        return api.services_list()

    def jsonrpc_service_info(self, service_name):
        return api.service_info(service_name)

    def jsonrpc_service_start(self, service_name):
        return api.service_start(service_name)

    def jsonrpc_service_stop(self, service_name):
        return api.service_stop(service_name)

    def jsonrpc_packets_stats(self):
        return api.packets_stats()

    def jsonrpc_packets_list(self):
        return api.packets_list()

    def jsonrpc_connections_list(self, wanted_protos=None):
        return api.connections_list(wanted_protos)

    def jsonrpc_streams_list(self, wanted_protos=None):
        return api.streams_list(wanted_protos)

    def jsonrpc_ping(self, idurl, timeout=10):
        return api.ping(str(idurl), timeout)

    def jsonrpc_user_ping(self, idurl, timeout=10):
        return api.user_ping(str(idurl), timeout)

    def jsonrpc_user_search(self, nickname):
        return api.user_search(nickname)

    def jsonrpc_message_send(self, recipient, message_body):
        return api.message_send(recipient, message_body)

    def jsonrpc_message_receive(self, consumer_id):
        return api.message_receive(consumer_id)

    def jsonrpc_receive_one_message(self):
        return api.receive_one_message()

    def jsonrpc_send_message(self, recipient, message_body):
        return api.send_message(recipient, message_body)

#     def jsonrpc_list_messages(self):
#         return api.list_messages()

#     def jsonrpc_list_correspondents(self):
#         return api.list_correspondents()

#     def jsonrpc_add_correspondent(self, idurl, nickname=''):
#         return api.add_correspondent(idurl, nickname)

#     def jsonrpc_remove_correspondent(self, idurl):
#         return api.remove_correspondent(idurl)

    def jsonrpc_find_peer_by_nickname(self, nickname):
        return api.find_peer_by_nickname(nickname)

    def jsonrpc_set_my_nickname(self, nickname):
        return api.set_my_nickname(nickname)

    def jsonrpc_broadcast_send_message(self, payload):
        return api.broadcast_send_message(payload)

    def jsonrpc_event_send(self, event_id, json_data=None):
        return api.event_send(event_id, json_data=json_data)

    def jsonrpc_network_stun(self, udp_port=None, dht_port=None):
        return api.network_stun(udp_port=udp_port, dht_port=dht_port)

    def jsonrpc_network_reconnect(self):
        return api.network_reconnect()

    def jsonrpc_reconnect(self):  # alias
        return api.network_reconnect()

#------------------------------------------------------------------------------


if __name__ == "__main__":
    lg.set_debug_level(20)
    init()
    reactor.run()
