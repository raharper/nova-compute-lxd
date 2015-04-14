# Copyright (c) 2015 Canonical Ltd
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

import mock
from nova import test
import requests

from nclxd.nova.virt.lxd import client


class LXDFakeResponse(object):
    """Fake response to LXD API."""

    def __init__(self, code=None, text=None):
        self.status_code = code
        self.text = text

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        if self.status_code > 300:
            raise requests.exception.HTTPError


class LXDTestClient(test.TestCase):
    def setUp(self):
        super(LXDTestClient, self).setUp()

        self.client = client.Client('https://127.0.0.1:8443',
                                    'client',
                                    'key')

    def test_client_defined(self):
        requests.get = mock.Mock(return_value=True)
        instance = self.client.defined('test')
        self.assertTrue(instance)

    def test_client_state(self):
        return_text = json.dumps({"type": "sync", "result": "success",
                                  "metadata": {"state": "RUNNING",
                                               "state_code": 3}})
        get_return = LXDFakeResponse(code=200,
                                     text=return_text)
        requests.get = mock.Mock(return_value=get_return)
        instance = self.client.state('test')
        self.assertIn('RUNNING', instance)

    def test_client_running(self):
        return_text = json.dumps({"type": "sync", "result": "success",
                                  "metadata": {"state": "RUNNING",
                                               "state_code": 3}})
        get_return = LXDFakeResponse(code=200,
                                     text=return_text)
        requests.get = mock.Mock(return_value=get_return)
        instance = self.client.running('test')
        self.assertTrue(instance)

    def test_client_list(self):
        return_text = json.dumps({"type": "sync", "result": "success",
                                  "metadata":
                                 ["dc5a4fd8-a43e-486f-9e2c-fb07917f2915"]})
        get_return = LXDFakeResponse(code=200,
                                     text=return_text)
        requests.get = mock.Mock(return_value=get_return)
        instance = self.client.list()
        self.assertIsInstance(instance, list)
        self.assertIn('dc5a4fd8-a43e-486f-9e2c-fb07917f2915', instance)

    def test_client_start(self):
        return_text = json.dumps({"type": "sync", "result": "success",
                                  "metadata": {"state": "RUNNING",
                                               "state_code": 3}})
        get_return = LXDFakeResponse(code=200,
                                     text=return_text)
        requests.put = mock.Mock(return_value=get_return)
        instance = self.client.start('test')
        self.assertTrue(instance)

    def test_client_stop(self):
        return_text = json.dumps({"type": "sync", "result": "success",
                                  "metadata": {"state": "RUNNING",
                                               "state_code": 3}})
        get_return = LXDFakeResponse(code=200,
                                     text=return_text)
        requests.put = mock.Mock(return_value=get_return)
        instance = self.client.start('test')
        self.assertTrue(instance)

    def test_client_reboot(self):
        return_text = json.dumps({"type": "sync", "result": "success",
                                  "metadata": {"state": "RUNNING",
                                               "state_code": 3}})
        get_return = LXDFakeResponse(code=200,
                                     text=return_text)
        requests.put = mock.Mock(return_value=get_return)
        instance = self.client.reboot('test')
        self.assertTrue(instance)

    def test_client_pause(self):
        return_text = json.dumps({"type": "sync", "result": "success",
                                  "metadata": {"state": "RUNNING",
                                               "state_code": 3}})
        get_return = LXDFakeResponse(code=200,
                                     text=return_text)
        requests.put = mock.Mock(return_value=get_return)
        instance = self.client.pause('test')
        self.assertTrue(instance)

    def test_client_unpause(self):
        return_text = json.dumps({"type": "sync", "result": "success",
                                  "metadata": {"state": "RUNNING",
                                               "state_code": 3}})
        get_return = LXDFakeResponse(code=200,
                                     text=return_text)
        requests.put = mock.Mock(return_value=get_return)
        instance = self.client.unpause('test')
        self.assertTrue(instance)
