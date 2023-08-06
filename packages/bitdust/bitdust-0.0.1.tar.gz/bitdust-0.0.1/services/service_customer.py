#!/usr/bin/python
# service_customer.py
#
# Copyright (C) 2008-2016 Veselin Penev, http://bitdust.io
#
# This file (service_customer.py) is part of BitDust Software.
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

module:: service_customer
"""

from services.local_service import LocalService


def create_service():
    return CustomerService()


class CustomerService(LocalService):

    service_name = 'service_customer'
    config_path = 'services/customer/enabled'

    def dependent_on(self):
        return ['service_p2p_hookups',
                ]

    def start(self):
        from customer import supplier_connector
        from contacts import contactsdb
        for supplier_idurl in contactsdb.suppliers():
            if supplier_idurl and not supplier_connector.by_idurl(
                    supplier_idurl):
                supplier_connector.create(supplier_idurl)
        return True

    def stop(self):
        from customer import supplier_connector
        for sc in supplier_connector.connectors().values():
            sc.automat('shutdown')
        return True
