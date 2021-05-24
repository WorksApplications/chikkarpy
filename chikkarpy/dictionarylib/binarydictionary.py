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

from .dictionaryheader import DictionaryHeader
from .dictionaryversion import is_dictionary
from .doublearraytrie import DoubleArrayTrie


class BinaryDictionary(object):

    def __init__(self, bytes_, header, trie, offset):
        """Constructs a new dictionary.

        Args:
            bytes_ (mmap.mmap): a memory-mapped dictionary
            header (DictionaryHeader): a header of dictionary
            trie (DoubleArrayTrie): a double array trie
            offset (int): byte offset
        """
        self._bytes = bytes_
        self._header = header
        self._trie = trie
        self._offset = offset

    @staticmethod
    def _read_dictionary(filename, access=mmap.ACCESS_READ):
        """Reads the synonym dictionary from the specified file.

        Args:
            filename (str): the file path of a synonym dictionary
            access (int): file-open mode

        Returns:
            tuple[mmap.mmap, DictionaryHeader, DoubleArrayTrie, int]: byte data to be read
        """
        with open(filename, 'rb') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=access)
        offset = 0

        header = DictionaryHeader.from_bytes(bytes_, offset)
        offset += header.storage_size()

        if not is_dictionary(header.version):
            raise Exception('invalid dictionary version')

        trie = DoubleArrayTrie(bytes_, offset)
        offset += trie.get_storage_size()

        return bytes_, header, trie, offset

    @classmethod
    def from_system_dictionary(cls, filename):
        """Constructs a new dictionary and return a ``BinaryDictionary`` object.

        Args:
            filename (str): the file path of a synonym dictionary

        Returns:
            BinaryDictionary: a binary dictionary
        """
        args = cls._read_dictionary(filename)
        return cls(*args)

    def close(self):
        del self._trie
        self._bytes.close()

    @property
    def bytes_(self):
        """mmap.mmap: a memory-mapped dictionary"""
        return self._bytes

    @property
    def header(self):
        """DictionaryHeader: a header of dictionary"""
        return self._header

    @property
    def trie(self):
        """DoubleArrayTrie: a double array trie"""
        return self._trie

    @property
    def offset(self):
        """int: byte offset"""
        return self._offset
