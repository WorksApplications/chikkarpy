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
from chikkarpy.dictionarylib.doublearraytrie import DoubleArrayTrie


class TestDoubleArrayTrie(TestCase):

    ENCODING = "utf-8"

    def setUp(self):
        dic_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'resources', 'system.dic')
        with open(dic_file, 'rb') as f:
            bytes_ = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        header = DictionaryHeader.from_bytes(bytes_, 0)
        self.trie = DoubleArrayTrie(bytes_, header.storage_size())

    def test_common_prefix_search(self):
        results = list(self.trie.lookup_by_common_prefix("open".encode(self.ENCODING), 0))
        self.assertEqual(len(results), 2)
        r1, r2 = results
        self.assertEqual(r1[0], 6)
        self.assertEqual(r1[1], 4)
        self.assertEqual(r2[0], 100006)
        self.assertEqual(r2[1], 4)

    def test_exact_match(self):
        self.assertCountEqual(self.trie.lookup_by_exact_match("open".encode(self.ENCODING)), [6, 100006])
        self.assertFalse(self.trie.lookup_by_exact_match("nothing".encode(self.ENCODING)))

    def test_storage_size(self):
        self.assertEqual(self.trie.get_storage_size(), 1095)
