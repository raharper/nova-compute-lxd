#!/usr/bin/python

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
import optparse
import os
import subprocess
import tempfile
import time


def parse_argv():
    optparser = optparse.OptionParser()
    optparser.add_option('-i', '--image',
                         help='Path to image', dest='image', metavar='PATH')
    (opts, args) = optparser.parse_args()

    if not os.path.exists(opts.image):
        optparser.error('Unable to open file')

    return (opts, args)


def create_tarball():
    workdir = tempfile.mkdtemp()
    rootfs_dir = os.path.join(workdir, 'rootfs')
    os.mkdir(rootfs_dir)
    image = opts.image
    subprocess.call(['tar', '--anchored', '--numeric-owner',
                     '--exclude=dev/*', '-zxf', image,
                     '-C', rootfs_dir])

    epoch = time.time()
    metadata = {
        'architecutre': 'x86_64',
        'creation_date': int(epoch)
    }
    metadata_yaml = json.dumps(metadata, sort_keys=True,
                               indent=4, separators=(',', ': '),
                               ensure_ascii=False).encode('utf-8') + b"\n"
    metadata_file = os.path.join(workdir, 'metadata.yaml')
    with open(metadata_file, 'w') as fp:
        fp.write(metadata_yaml)
    source_tarball = image.split('.')
    dest_tarball = "%s-lxd.tar.gz" % source_tarball[0]
    subprocess.call(['tar', '-C', workdir, '-zcf',
                     dest_tarball, 'metadata.yaml', 'rootfs'])

if __name__ == '__main__':
    (opts, args) = parse_argv()

    create_tarball()
