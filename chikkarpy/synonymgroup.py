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

from .synonym import Synonym


class SynonymGroup(object):
    """
    A container of synonyms
    """
    def __init__(self, group_id, synonyms):
        """Constructs a new group with the specified synonym group ID and the list of synonyms.

        Args:
            group_id (int): a synonym group ID
            synonyms (list[Synonym]): a list of synonyms
        """
        self._group_id = group_id
        self._synonyms = synonyms

    def get_id(self):
        """Returns the ID of this group.

        Returns:
            int: the ID of this group
        """
        return self._group_id

    def get_synonyms(self):
        """Returns the list of synonyms in this group.

        Returns:
            list[Synonym]: the list of synonyms in this group
        """
        return self._synonyms

    def lookup(self, word):
        """Returns a synonym from this group with the specified headword.

        Args:
            word (str): a headword

        Returns:
            Synonym | None: the synonym with the specified headword, or ``None`` if a synonym is not found
        """
        for synonym in self._synonyms:
            if synonym.head_word == word:
                return synonym

        return None
