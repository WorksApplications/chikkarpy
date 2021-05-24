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

from chikkarpy import Chikkar
from chikkarpy.dictionarylib import Dictionary


class TestChikkar(TestCase):

    def setUp(self):
        dict_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

        self.system_dict = Dictionary(os.path.join(dict_dir, 'system.dic'), False)
        self.user_dict = Dictionary(os.path.join(dict_dir, 'user.dic'), True)
        self.user2_dict = Dictionary(os.path.join(dict_dir, 'user2.dic'), True)

        self.chikkar = Chikkar()
        self.chikkar.add_dictionary(self.system_dict)

    def tearDown(self):
        self.system_dict.dict_.close()
        self.user_dict.dict_.close()
        self.user2_dict.dict_.close()

    def test_find(self):
        self.assertCountEqual(self.chikkar.find("開店"), ["始業", "営業開始", "店開き", "オープン", "open"])
        self.assertFalse(self.chikkar.find("オープン"))
        self.assertFalse(self.chikkar.find("nothing"))

    def test_find_with_group_ids(self):
        group_ids = [6]
        self.assertCountEqual(self.chikkar.find("開店", group_ids=group_ids), ["始業", "営業開始", "店開き", "オープン", "open"])
        self.assertFalse(self.chikkar.find("オープン", group_ids=group_ids))
        self.assertFalse(self.chikkar.find("nothing", group_ids=[0]))

    def test_find_oov_with_group_ids(self):
        with self.assertRaises(ValueError):
            self.assertFalse(self.chikkar.find("nothing", group_ids=[6]))

    def test_find_with_user_dict(self):
        self.chikkar.add_dictionary(self.user_dict)
        self.assertCountEqual(self.chikkar.find("open"), ["開放", "オープン"])
        self.chikkar.add_dictionary(self.user2_dict)
        self.assertFalse(self.chikkar.find("open"))
        self.assertCountEqual(self.chikkar.find("開店"), ["始業", "営業開始", "店開き", "オープン", "open"])

    def test_enable_verb(self):
        self.chikkar.add_dictionary(self.user_dict)
        self.chikkar.enable_verb()
        self.assertCountEqual(self.chikkar.find("open"), ["開放", "開け放す", "開く", "オープン"])
