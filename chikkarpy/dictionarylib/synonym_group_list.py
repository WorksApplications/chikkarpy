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

import struct

from ..dictionarylib.flags import Flags
from ..synonym import Synonym
from ..synonymgroup import SynonymGroup


class SynonymGroupList(object):

    def __init__(self, bytes_, offset):
        """Constructs a new synonym group list.

        Args:
            bytes_ (mmap.mmap): a memory-mapped dictionary
            offset (int): byte offset
        """
        self.bytes_ = bytes_
        self.orig_pos = self.bytes_.tell()
        self.bytes_.seek(offset)
        self.size = int.from_bytes(self.bytes_.read(4), 'little', signed=True)

        self.group_id_to_offset = {}
        for i in range(self.size):
            group_id = int.from_bytes(self.bytes_.read(4), 'little', signed=True)
            offset = int.from_bytes(self.bytes_.read(4), 'little', signed=True)
            self.group_id_to_offset[group_id] = offset

    def get_synonym_group(self, group_id):
        """Search a synonym group with the ``group_id`` and return the ``SynonymGroup`` object.

        Args:
            group_id (int): a synonym group ID

        Returns:
            SynonymGroup | None: the ``SynonymGroup`` with the ``group_id``, or ``None`` if no group is found.
        """
        if group_id not in self.group_id_to_offset:
            return None

        offset = self.group_id_to_offset[group_id]
        self.bytes_.seek(offset)  # ? self.bytes_.seek(self.group_id_to_offset[group_id])

        synonyms = []
        n = int.from_bytes(self.bytes_.read(2), 'little')
        for i in range(n):
            head_word = self.buffer_to_string()
            lexeme_ids = self.buffer_to_short_array()
            flags = int.from_bytes(self.bytes_.read(2), 'little')
            category = self.buffer_to_string()
            synonyms.append(Synonym(head_word, lexeme_ids, Flags.from_int(flags), category))

        return SynonymGroup(group_id, synonyms)

    def buffer_to_string_length(self):
        """Reads a byte with a length of a subsequent string and returns the string length.

        Returns:
            int: a string length
        """
        length = self.bytes_.read_byte()
        if length < 128:
            return length
        else:
            low = self.bytes_.read_byte()
            return ((length & 0x7F) << 8) | low

    def buffer_to_string(self):
        """Reads bytes with a string of the appropriate length and returns the string.

        Returns:
            str: a string
        """
        length = self.buffer_to_string_length()
        return self.bytes_.read(2 * length).decode('utf-16-le')

    def buffer_to_short_array(self):
        """Reads byte with a continuous value of short.

        Returns:
            list[int]: a list of short
        """
        length = self.bytes_.read_byte()
        _bytes = self.bytes_.read(2 * length)
        return list(struct.unpack('{}h'.format(length), _bytes))
