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

from io import BufferedWriter, TextIOWrapper
from logging import DEBUG, StreamHandler, getLogger

from dartsclone import DoubleArray

from sortedcontainers import SortedDict

from .flags import Flags
from .format import Acronym, Ambiguity, Column, Form, IsNoun, Variant
from .jtypedbytebuffer import JTypedByteBuffer
from ..synonym import Synonym


class SynonymWithGroupId:
    def __init__(self, group_id, synonym):
        """Constructs a synonym with its group ID

        Args:
            group_id (int): a group ID
            synonym (Synonym): a synonym object
        """
        self._synonym = synonym
        self._group_id = group_id

    @property
    def group_id(self):
        return self._group_id

    @property
    def headword(self):
        return self._synonym.head_word

    @property
    def lexeme_ids(self):
        return self._synonym.lexeme_ids

    @property
    def flags(self):
        return self._synonym.flags

    @property
    def category(self):
        return self._synonym.category


class DictionaryBuilder:
    __BYTE_MAX_VALUE = 127

    @staticmethod
    def __default_logger():
        """Sets and returns a default logging.

        Returns:
            StreamHandler: a default logging
        """
        handler = StreamHandler()
        handler.terminator = ""
        handler.setLevel(DEBUG)
        logger = getLogger(__name__)
        logger.setLevel(DEBUG)
        logger.addHandler(handler)
        logger.propagate = False

        return logger

    def __init__(self, *, logger=None):
        self.byte_buffer = JTypedByteBuffer()
        self.trie_keys = SortedDict()
        self.synonym_groups = []
        self.is_dictionary = False
        self.logger = logger or self.__default_logger()

    def build(self, input_path, out_stream):
        """Builds the synonym dictionary from the specified input file and writes it to the specified output.

        Args:
            input_path (str): an input file path
            out_stream (BufferedWriter):
        """
        self.logger.info('reading the source file...')
        with open(input_path, 'r', encoding='utf-8') as rf:
            self.build_synonym(rf)
        self.write_trie(out_stream)
        self.write_synonym_groups(out_stream)

    def build_synonym(self, synonym_input_stream):
        """Reads lines in the specified input file.

        Args:
            synonym_input_stream (TextIOWrapper): an input stream

        Raises:
            ValueError: Group ID is changed in a group.
        """
        block = []
        line_no = -1
        group_id = -1
        try:
            for i, row in enumerate(synonym_input_stream):
                line_no = i
                if not row or row.isspace():
                    if len(block) == 0:
                        continue
                    else:
                        self.synonym_groups.append(block)
                        block = []
                        group_id = -1
                else:
                    entry = self.parse_line(row)
                    if not entry:
                        continue
                    if group_id < 0:
                        group_id = entry.group_id
                    elif group_id != entry.group_id:
                        raise ValueError("Group ID is changed in block.")
                    self.add_to_trie(entry.headword, group_id)
                    block.append(entry)
            if len(block) > 0:
                self.synonym_groups.append(block)
        except Exception as e:
            if line_no >= 0:
                self.logger.error(
                    '{} at line {} in {}\n'.format(e.args[0], line_no, synonym_input_stream.name))
            raise e

    def parse_line(self, line):
        """Parses a line in a dictionary file (csv).

        Args:
            line (str): each line in a csv file

        Returns:
            SynonymWithGroupId: encoded line

        Raises:
            ValueError: Too few columns in a specified line
        """
        cols = line.split(",")
        if len(cols) <= max(map(int, Column)):
            raise ValueError('Too few columns. {} <= n are allowed.'.format(max(map(int, Column))))
        if int(cols[Column.AMBIGUITY]) == Ambiguity.INVALID:
            return None

        group_id = int(cols[Column.GROUP_ID])

        lexeme_ids = cols[Column.GROUP_ID] if cols[Column.LEXEME_IDS] == "" else list(map(int, cols[Column.LEXEME_IDS].split("/")))
        headword = cols[Column.HEAD_WORD]
        _is_noun = self.parse_boolean(cols[Column.IS_NOUN], IsNoun.FALSE, IsNoun.TRUE)
        _has_ambiguity = self.parse_boolean(cols[Column.AMBIGUITY], Ambiguity.FALSE, Ambiguity.TRUE)
        _form_type = self.parse_int(cols[Column.FORM_TYPE], max(map(int, Form)))
        _acronym_type = self.parse_int(cols[Column.ACRONYM_TYPE], max(map(int, Acronym)))
        _variant_type = self.parse_int(cols[Column.VARIANT_TYPE], max(map(int, Variant)))
        flags = Flags(_has_ambiguity, _is_noun, _form_type, _acronym_type, _variant_type)
        category = cols[Column.CATEGORY]

        entry = SynonymWithGroupId(group_id, Synonym(headword, lexeme_ids, flags, category))

        return entry

    @staticmethod
    def parse_boolean(s, false_value, true_value):
        """Parses and validates a str-type boolean value.

        Args:
            s (str): a str-type boolean value
            false_value (int): false value
            true_value (int): true value

        Returns:
            bool: validated and parsed value

        Raises:
            ValueError: ``v`` is an invalid value
        """
        v = int(s)
        if v == false_value:
            return False
        elif v == true_value:
            return True
        else:
            raise ValueError("'{}' is an invalid value. '{}' or '{}' are allowed.".format(s, false_value, true_value))

    @staticmethod
    def parse_int(s, limit):
        """Parses and validates a str-type numeric value.

        Args:
            s (str): a str-type numeric value
            limit (int): an allowed maximum value

        Returns:
            int: validated and parsed value
        """
        v = int(s)
        if v < 0 or v > limit:
            raise ValueError("'{}' is an invalid value. 0 <= n <= '{}' are allowed.".format(s, limit))
        return v

    def add_to_trie(self, headword, group_id):
        """Adds ``headword``-``group_id`` pairs to a trie.

        Args:
            headword (str): a headword
            group_id (int): a synonym group ID
        """
        key = headword.encode('utf-8')
        if key not in self.trie_keys:
            self.trie_keys[key] = []
        self.trie_keys[key].append(group_id)

    def write_trie(self, io_out):
        """Writes ``headword``-``group_id`` pairs to the specified output file.

        Args:
            io_out (BufferedWriter): an output stream
        """
        trie = DoubleArray()
        keys = []
        vals = []
        id_table = JTypedByteBuffer()
        for key, ids in self.trie_keys.items():
            keys.append(key)
            vals.append(id_table.tell())
            id_table.write_int(len(ids), 'byte')
            for _id in ids:
                id_table.write_int(_id, 'int')

        self.logger.info('building the trie...')
        trie.build(keys, lengths=[len(k) for k in keys], values=vals)
        self.logger.info('done\n')
        self.logger.info('writing the trie...')
        self.byte_buffer.clear()
        self.byte_buffer.write_int(trie.size(), 'int')
        self.byte_buffer.seek(0)
        io_out.write(self.byte_buffer.read())
        self.byte_buffer.clear()
        io_out.write(trie.array())
        self.__logging_size(trie.size() * 4 + 4)
        trie.clear()
        del trie

        self.logger.info('writing the word-ID table...')
        self.byte_buffer.write_int(id_table.tell(), 'int')
        self.byte_buffer.seek(0)
        io_out.write(self.byte_buffer.read())
        self.byte_buffer.clear()
        id_table.seek(0)
        io_out.write(id_table.read())
        self.__logging_size(id_table.tell() + 4)
        del id_table

    def write_synonym_groups(self, io_out):
        """Writes synonym groups to the specified output file.

        Args:
            io_out (BufferedWriter): an output stream
        """
        mark = io_out.tell()
        io_out.seek(mark + 4 * len(self.synonym_groups) * 2 + 4)
        offsets = JTypedByteBuffer()
        offsets.write_int(len(self.synonym_groups), 'int')
        self.logger.info('writing the word_infos...')
        base = io_out.tell()
        for entries in self.synonym_groups:
            if len(entries) == 0:
                continue
            offsets.write_int(entries[0].group_id, 'int')
            offsets.write_int(io_out.tell(), 'int')

            self.byte_buffer.write_int(len(entries), 'short')
            for entry in entries:
                self.write_string(entry.headword)
                self.write_short_array(entry.lexeme_ids)
                self.byte_buffer.write_int(entry.flags.encode(), 'short')
                self.write_string(entry.category)
            self.byte_buffer.seek(0)
            io_out.write(self.byte_buffer.read())
            self.byte_buffer.clear()

        self.__logging_size(io_out.tell() - base)
        self.logger.info('writing synonym groups offsets...')
        io_out.seek(mark)
        offsets.seek(0)
        io_out.write(offsets.read())
        self.__logging_size(offsets.tell())

    def write_string(self, text):
        """Converts a string to bytes and writes it to a buffer.

        Args:
            text (str): a string
        """
        len_ = 0
        for c in text:
            if 0x10000 <= ord(c) <= 0x10FFFF:
                len_ += 2
            else:
                len_ += 1
        self.write_string_length(len_)
        self.byte_buffer.write_str(text)

    def write_short_array(self, array):
        """Converts a list of short to bytes and writes it to a buffer.

        Args:
            array (list[int]): a list of short
        """
        self.byte_buffer.write_int(len(array), 'byte')
        for item in array:
            self.byte_buffer.write_int(item, 'short')

    def write_string_length(self, len_):
        """Converts a length of a string and writes it to a buffer.

        Args:
            len_ (int): a length of a string
        """
        if len_ <= self.__BYTE_MAX_VALUE:
            self.byte_buffer.write_int(len_, 'byte')
        else:
            self.byte_buffer.write_int((len_ >> 8) | 0x80, 'byte')
            self.byte_buffer.write_int((len_ & 0xFF), 'byte')

    def __logging_size(self, size):
        self.logger.info('{} bytes\n'.format(size))
