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

from .binarydictionary import BinaryDictionary
from .synonym_group_list import SynonymGroupList
from ..config import get_system_dictionary_path
from ..synonymgroup import SynonymGroup


class Dictionary(object):
    """
    A container of synonyms
    """
    def __init__(self, filename=None, enable_trie=False):
        """Reads the synonym dictionary from the specified file.

        If ``enableTrie`` is ``False``, a search by synonym group IDs takes precedence over a search by the headword.

        Args:
            filename (str | None): path of synonym dictionary file
            enable_trie (bool): ``True`` to enable trie, otherwise ``False``
        """
        self.filename = filename if filename is not None else get_system_dictionary_path()
        self.dict_ = BinaryDictionary.from_system_dictionary(self.filename)
        self.enable_trie = enable_trie
        self.group_list = SynonymGroupList(self.dict_.bytes_, self.dict_.offset)

    def lookup(self, word, group_ids):
        """Returns a synonym group ID that contains the specified headword or a specified synonym group ID.

        Args:
            word (str): a headword to search for
            group_ids (list[int] | None): an array of synonym group IDs to search for

        Returns:
            list[int]: an array of synonym group IDs found, or an empty array if not found
        """
        if self.enable_trie or group_ids is None:
            return self.dict_.trie.lookup_by_exact_match(word.encode('utf-8'))
        else:
            return group_ids

    def get_synonym_group(self, group_id):
        """Returns a group of synonyms with the specified ID.

        Args:
            group_id (int): a synonym group ID

        Returns:
            SynonymGroup | None: the group of synonyms with the specified ID, or None if no ID matches
        """
        return self.group_list.get_synonym_group(group_id)

    def close(self):
        self.dict_.close()
