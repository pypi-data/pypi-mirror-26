#!/usr/bin/python
# message_keeper.py
#
# Copyright (C) 2008-2016 Veselin Penev, http://bitdust.io
#
# This file (message_keeper.py) is part of BitDust Software.
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
.. module:: message_keeper

"""

#------------------------------------------------------------------------------

_Debug = True
_DebugLevel = 10

#------------------------------------------------------------------------------

import os

#------------------------------------------------------------------------------

from logs import lg

from system import bpio

from main import settings

from interface import api

from services import driver

from crypt import my_keys

from userid import my_id
from userid import global_id

from chat import message

#------------------------------------------------------------------------------

def init():
    lg.out(4, "message_keeper.init")
    message.AddIncomingMessageCallback(on_incoming_message)
    message.AddOutgoingMessageCallback(on_outgoing_message)
    if not my_keys.is_key_registered(messages_key_id()):
        my_keys.generate_key(messages_key_id())


def shutdown():
    lg.out(4, "message_keeper.shutdown")
    message.RemoveIncomingMessageCallback(on_incoming_message)
    message.RemoveOutgoingMessageCallback(on_outgoing_message)

#------------------------------------------------------------------------------

def messages_key_id():
    return global_id.MakeGlobalID(key_alias='messages', customer=my_id.getGlobalID())

#------------------------------------------------------------------------------

def on_incoming_message(packet_in_object, private_message_object, decrypted_message_body):
    """
    """
    save_incoming_message(private_message_object, packet_in_object.PacketID)


def on_outgoing_message(message_body, private_message_object, remote_identity, outpacket, packet_out_object):
    """
    """
    save_outgoing_message(private_message_object, outpacket.PacketID)

#------------------------------------------------------------------------------

def save_incoming_message(private_message_object, message_id):
    """
    """
    if not driver.is_started('service_backups'):
        lg.warn('service_backups is not started')
        return False
    serialized_message = private_message_object.serialize()
    local_msg_folder = os.path.join(settings.getMessagesDir(), private_message_object.recipient, 'in')
    if not bpio._dir_exist(local_msg_folder):
        bpio._dirs_make(local_msg_folder)
    local_msg_filename = os.path.join(local_msg_folder, message_id)
    if not bpio.WriteFile(local_msg_filename, serialized_message):
        lg.warn('failed writing incoming message locally')
        return False
    remote_path_for_message = os.path.join('.messages', 'in', private_message_object.recipient, message_id)
    global_message_path = global_id.MakeGlobalID(customer=messages_key_id(), path=remote_path_for_message)
    res = api.file_create(global_message_path)
    if res['status'] != 'OK':
        lg.warn('failed to create path "%s" in the catalog: %s' % (
            global_message_path, res['errors']))
        return False
    res = api.file_upload_start(local_msg_filename, global_message_path, wait_result=False)
    if res['status'] != 'OK':
        lg.warn('failed to upload message "%s": %s' % (global_message_path, res['errors']))
        return False
    return True

def save_outgoing_message(private_message_object, message_id):
    """
    """
    if not driver.is_started('service_backups'):
        lg.warn('service_backups is not started')
        return False
    serialized_message = private_message_object.serialize()
    local_msg_folder = os.path.join(settings.getMessagesDir(), private_message_object.recipient, 'out')
    if not bpio._dir_exist(local_msg_folder):
        bpio._dirs_make(local_msg_folder)
    local_msg_filename = os.path.join(local_msg_folder, message_id)
    if not bpio.WriteFile(local_msg_filename, serialized_message):
        lg.warn('failed writing outgoing message locally')
        return False
    remote_path_for_message = os.path.join('.messages', 'out', private_message_object.recipient, message_id)
    global_message_path = global_id.MakeGlobalID(customer=messages_key_id(), path=remote_path_for_message)
    res = api.file_create(global_message_path)
    if res['status'] != 'OK':
        lg.warn('failed to create path "%s" in the catalog: %s' % (
            global_message_path, res['errors']))
        return False
    res = api.file_upload_start(local_msg_filename, global_message_path, wait_result=False)
    if res['status'] != 'OK':
        lg.warn('failed to upload message "%s": %s' % (global_message_path, res['errors']))
        return False
    return True
