#!/usr/bin/python
# rest_http_server.py
#
# Copyright (C) 2008-2016 Veselin Penev, http://bitdust.io
#
# This file (rest_http_server.py) is part of BitDust Software.
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

module:: rest_http_server
"""

#------------------------------------------------------------------------------

import cgi
import json

#------------------------------------------------------------------------------

from twisted.internet import reactor
from twisted.web.server import Site

#------------------------------------------------------------------------------

from logs import lg

from interface import api

from lib.txrestapi.txrestapi.resource import APIResource
from lib.txrestapi.txrestapi.methods import GET, POST, PUT, DELETE, ALL

#------------------------------------------------------------------------------

_APIListener = None

#------------------------------------------------------------------------------

def init(port=None):
    global _APIListener
    if _APIListener is not None:
        lg.warn('_APIListener already initialized')
        return
    if not port:
        port = 8180
    try:
        api_resource = BitDustRESTHTTPServer()
        site = BitDustAPISite(api_resource, timeout=None)
        _APIListener = reactor.listenTCP(port, site)
    except:
        lg.exc()
    lg.out(4, 'rest_http_server.init')


def shutdown():
    global _APIListener
    if _APIListener is None:
        lg.warn('_APIListener is None')
        return
    lg.out(4, 'rest_http_server.shutdown calling _APIListener.stopListening()')
    _APIListener.stopListening()
    del _APIListener
    _APIListener = None
    lg.out(4, '    _APIListener destroyed')

#------------------------------------------------------------------------------

def _request_arg(request, key, default='', mandatory=False):
    """
    Simplify extracting arguments from url query in request.
    """
    args = request.args or {}
    if key in args:
        values = args.get(key, [default, ])
        return values[0] if values else default
    if mandatory:
        raise Exception('mandatory url query argument missed: %s' % key)
    return default


def _request_data(request, mandatory_keys=[]):
    """
    Simplify extracting input parameters from request body.
    """
    try:
        data = json.loads(request.content.getvalue())
    except:
        raise Exception('invalid json input')
    for k in mandatory_keys:
        if k not in data:
            raise Exception('one of mandatory parameters missed: %s' % mandatory_keys)
    return data

#------------------------------------------------------------------------------

class BitDustAPISite(Site):

    def buildProtocol(self, addr):
        """
        Only accepting connections from local machine!
        """
        if addr.host != '127.0.0.1':
            return None
        return Site.buildProtocol(self, addr)


class BitDustRESTHTTPServer(APIResource):
    """
    A set of API method to interract and control locally running BitDust process.
    """

    #------------------------------------------------------------------------------

    @GET('^/process/stop/v1$')
    def process_stop(self, request):
        return api.stop()

    @GET('^/process/restart/v1$')
    def process_restart(self, request):
        return api.restart(showgui=bool(request.args.get('showgui')))

    @GET('^/process/show/v1$')
    def process_show(self, request):
        return api.show()

    #------------------------------------------------------------------------------

    @GET('^/config/v1$')
    @GET('^/config/list/v1$')
    def config_list_v1(self, request):
        return api.config_list(sort=True)

    @GET('^/config/get/(?P<key1>[^/]+)/(?P<key2>[^/]+)/(?P<key3>[^/]+)/v1$')
    def config_get_l3_v1(self, request, key1, key2, key3):
        return api.config_get(key=(key1 + '/' + key2 + '/' + key3))

    @GET('^/config/get/(?P<key1>[^/]+)/(?P<key2>[^/]+)/v1$')
    def config_get_l2_v1(self, request, key1, key2):
        return api.config_get(key=(key1 + '/' + key2))

    @GET('^/config/get/(?P<key>[^/]+)/v1$')
    def config_get_l1_v1(self, request, key):
        return api.config_get(key=key)

    @GET('^/config/get/v1$')
    def config_get_v1(self, request):
        return api.config_get(key=cgi.escape(dict({} or request.args).get('key', [''])[0]),)

    @POST('^/config/set/(?P<key1>[^/]+)/(?P<key2>[^/]+)/(?P<key3>[^/]+)/v1$')
    def config_set_l3_v1(self, request, key1, key2, key3):
        data = _request_data(request, mandatory_keys=['value', ])
        return api.config_set(key=(key1 + '/' + key2 + '/' + key3), value=data['value'])

    @POST('^/config/set/(?P<key1>[^/]+)/(?P<key2>[^/]+)/v1$')
    def config_set_l2_v1(self, request, key1, key2):
        data = _request_data(request, mandatory_keys=['value', ])
        return api.config_set(key=(key1 + '/' + key2), value=data['value'])

    @POST('^/config/set/(?P<key>[^/]+)/v1$')
    def config_set_l1_v1(self, request, key):
        data = _request_data(request, mandatory_keys=['value', ])
        return api.config_set(key=key, value=data['value'])

    @POST('^/config/set/v1$')
    def config_set_v1(self, request):
        data = _request_data(request, mandatory_keys=['value', ])
        return api.config_set(key=data['key'], value=data['value'])

    #------------------------------------------------------------------------------

    @GET('^/network/reconnect/v1$')
    def network_reconnect_v1(self, request):
        return api.network_reconnect()

    @GET('^/network/stun/v1$')
    def network_stun_v1(self, request):
        return api.network_stun()

    #------------------------------------------------------------------------------

    @GET('^/key/v1$')
    @GET('^/key/list/v1$')
    def key_list_v1(self, request):
        return api.keys_list(
            sort=bool(_request_arg(request, 'sort', '0') != '0'),
            include_private=bool(_request_arg(request, 'include_private', '0') != '0'), )

    @GET('^/key/get/(?P<key_id>[^/]+)/v1$')
    def key_get_arg_v1(self, request, key_id):
        return api.key_get(
            key_id=key_id,
            include_private=bool(_request_arg(request, 'include_private', '0') != '0'), )

    @GET('^/key/get/v1$')
    def key_get_v1(self, request):
        return api.key_get(
            key_id=_request_arg(request, 'key_id', mandatory=True),
            include_private=bool(_request_arg(request, 'include_private', '0') != '0'), )

    @POST('^/key/create/v1$')
    def key_create_v1(self, request):
        data = _request_data(request, mandatory_keys=['alias', ])
        return api.key_create(
            key_alias=data['alias'],
            key_size=int(data.get('size', 4096)),
            include_private=bool(data.get('include_private')), )

    @DELETE('^/key/erase/(?P<key_id>[^/]+)/v1$')
    def key_erase_arg_v1(self, request, key_id):
        return api.key_erase(key_id)

    @DELETE('^/key/erase/v1$')
    def key_erase_v1(self, request):
        data = _request_data(request, mandatory_keys=['key_id', ])
        return api.key_erase(key_id=data['key_id'])

    @PUT('^/key/share/(?P<key_id>[^/]+)/v1$')
    def key_share_arg_v1(self, request, key_id):
        data = _request_data(request, mandatory_keys=['trusted_user', ])
        return api.key_share(key_id=key_id, trusted_global_id_or_idurl=data['trusted_user'])

    @PUT('^/key/share/v1$')
    def key_share_v1(self, request):
        data = _request_data(request, mandatory_keys=['key_id', 'trusted_user', ])
        return api.key_share(key_id=data['key_id'], trusted_global_id_or_idurl=data['trusted_user'])

    #------------------------------------------------------------------------------

    @GET('^/file/v1$')
    @GET('^/file/list/v1$')
    def file_list_v1(self, request):
        return api.files_list(remote_path=_request_arg(request, 'remote_path', None))

    @GET('^/file/info/v1$')
    def file_info_v1(self, request):
        return api.file_info(
            remote_path=_request_arg(request, 'remote_path', mandatory=True),
            include_uploads=bool(_request_arg(request, 'include_uploads', '1') != '0'),
            include_downloads=bool(_request_arg(request, 'include_downloads', '1') != '0'), )

    @POST('^/file/create/v1$')
    def file_create_v1(self, request):
        data = _request_data(request, mandatory_keys=['remote_path', ])
        return api.file_create(
            remote_path=data['remote_path'],
            as_folder=data.get('as_folder', False), )

    @DELETE('^/file/delete/v1$')
    def file_delete_v1(self, request):
        data = _request_data(request, mandatory_keys=['remote_path', ])
        return api.file_delete(remote_path=data['remote_path'])

    @GET('^/file/upload/v1$')
    def files_uploads_v1(self, request):
        return api.files_uploads(
            include_running=bool(_request_arg(request, 'include_running', '1') != '0'),
            include_pending=bool(_request_arg(request, 'include_pending', '1') != '0'), )

    @POST('^/file/upload/start/v1$')
    def file_upload_start_v1(self, request):
        data = _request_data(request, mandatory_keys=['local_path', 'remote_path', ])
        return api.file_upload_start(
            local_path=data['local_path'],
            remote_path=data['remote_path'],
            wait_result=data.get('wait_result', True), )

    @POST('^/file/upload/stop/v1$')
    def file_upload_stop_v1(self, request):
        data = _request_data(request, mandatory_keys=['remote_path', ])
        return api.file_upload_stop(remote_path=data['remote_path'])

    @GET('^/file/sync/v1$')
    def file_sync_v1(self, request):
        return api.files_sync()

    #------------------------------------------------------------------------------

    @ALL('^/*')
    def not_found(self, request):
        return api.ERROR('method %s:%s not found' % (request.method, request.path))

#------------------------------------------------------------------------------
