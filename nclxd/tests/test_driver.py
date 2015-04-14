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

import fixtures
import mock
from nova import test
from nova.tests.unit.image import fake as fake_image
from nova.tests.unit import utils
from oslo.config import cfg

from nclxd.nova.virt.lxd import client
from nclxd.nova.virt.lxd import container
from nclxd.nova.virt.lxd import driver

CONF = cfg.CONF
CONF.import_opt('image_cache_subdirectory_name', 'nova.virt.imagecache')


class LXDTestDriver(test.TestCase):
    def setUp(self):
        super(LXDTestDriver, self).setUp()

        self.ctxt = utils.get_test_admin_context()
        fake_image.stub_out_image_service(self.stubs)

        self.flags(lxd_root_dir=self.useFixture(
                   fixtures.TempDir()).path,
                   group='lxd')
        self.driver = driver.LXDDriver(None, None)

    @mock.patch.object(client.Client, 'list')
    def test_list_instances(self, mock_list):
        mock_list.return_value = ['container1']
        domains = self.driver.list_instances()
        self.assertIsInstance(domains, list)

    @mock.patch.object(client.Client, 'list')
    def test_list_instances_uuid(self, mock_list):
        mock_list.return_value = ['container1']
        domains = self.driver.list_instances()
        self.assertIsInstance(domains, list)

    @mock.patch.object(container.Container, '_fetch_image')
    @mock.patch.object(container.Container, '_start_container')
    def test_spawn_container(self, image_info=None, instance_href=None,
                             network_info=None):
        instance_href = utils.get_test_instance()
        image_info = utils.get_test_image_info(None, instance_href)
        network_info = utils.get_test_network_info()
        self.driver.spawn(self.ctxt, instance_href, image_info,
                          'fake_files', 'fake_password',
                          network_info=network_info)

    @mock.patch.object(container.Container, '_fetch_image')
    @mock.patch.object(container.Container, '_start_container')
    @mock.patch.object(client.Client, 'destroy')
    def test_destroy_container(self, image_info=None, instance_href=None,
                               network_info=None):
        instance_href = utils.get_test_instance()
        image_info = utils.get_test_image_info(None, instance_href)
        network_info = utils.get_test_network_info()
        self.driver.spawn(self.ctxt, instance_href, image_info,
                          'fake_files', 'fake_password',
                          network_info=network_info)
        self.driver.destroy(self.ctxt, instance_href, network_info, None, True)

    @mock.patch.object(container.Container, '_fetch_image')
    @mock.patch.object(container.Container, '_start_container')
    @mock.patch.object(client.Client, 'reboot')
    def test_reboot_container(self, image_info=None, instance_href=None,
                              network_info=None):
        reboot_type = "SOFT"
        instance_href = utils.get_test_instance()
        image_info = utils.get_test_image_info(None, instance_href)
        network_info = utils.get_test_network_info()
        self.driver.spawn(self.ctxt, instance_href, image_info,
                          'fake_files', 'fake_password',
                          network_info=network_info)
        self.driver.reboot(self.ctxt, instance_href, network_info,
                           reboot_type)
