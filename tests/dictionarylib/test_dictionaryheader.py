# Copyright (c) 2021 Works Applications Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mmap
import os
from unittest import TestCase

from chikkarpy.dictionarylib.dictionaryheader import DictionaryHeader
from chikkarpy.dictionarylib.dictionaryversion import SYSTEM_DICT_VERSION_1


class TestDictionaryHeader(TestCase):

    def setUp(self):
        dic_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'resources', 'system.dic')
        with open(dic_file, 'rb') as f:
            bytes_ = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        self.header = DictionaryHeader.from_bytes(bytes_, 0)

    def test_version(self):
        self.assertTrue(self.header.version, SYSTEM_DICT_VERSION_1)

    def test_create_time(self):
        self.assertTrue(self.header.create_time > 0)

    def test_description(self):
        self.assertEqual(self.header.description, "the system dictionary for the unit tests")

    def test_is_dictionary(self):
        self.assertTrue(self.header.is_dictionary())
