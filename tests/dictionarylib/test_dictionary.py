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

import os
from unittest import TestCase

from chikkarpy.dictionarylib import Dictionary


class TestDictionary(TestCase):

    def setUp(self):
        dic_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'resources', 'system.dic')
        self.dict = Dictionary(dic_file, True)
        self.dict_group_id = Dictionary(dic_file, False)

    def tearDown(self):
        self.dict.dict_.close()
        self.dict_group_id.dict_.close()

    def test_lookup(self):
        self.assertCountEqual(self.dict.lookup("open", group_ids=None), [6, 100006])
        self.assertCountEqual(self.dict.lookup("open", group_ids=[4]), [6, 100006])

        self.assertCountEqual(self.dict_group_id.lookup("open", group_ids=None), [6, 100006])
        self.assertCountEqual(self.dict_group_id.lookup("open", group_ids=[4]), [4])

    def test_get_synonyms(self):
        synonym_group = self.dict.get_synonym_group(6)
        self.assertTrue(synonym_group)
        self.assertEqual(synonym_group.get_id(), 6)

        # non-existent group id in the dictionary
        synonym_group = self.dict.get_synonym_group(200)
        self.assertFalse(synonym_group)
