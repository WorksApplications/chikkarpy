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

from .dictionarylib import Dictionary


class Chikkar(object):
    """
    A container of synonym dictionaries.
    """
    def __init__(self):
        self._dictionaries = []
        self._can_search_verb = False

    def enable_verb(self):
        """Enable verb and adjective synonyms.

        After this method is called, ``self.find()`` searches for synonyms for verbs and adjectives.
        """
        self._can_search_verb = True

    def add_dictionary(self, dictionary):
        """Add a synonym dictionary.

        Adds a ``dictionary`` to be used for search. When searching, the dictionary added later takes precedence.

        Args:
            dictionary (Dictionary): a synonym dictionary
        """
        self._dictionaries.insert(0, dictionary)

    def find(self, word, group_ids=None):
        """Returns synonyms for the specified word.

        If the tries in the dictionaries are enabled and ``group_ids`` is not ``None``,
        use the synonym group IDs as keys. Otherwise, use ``word`` as a key.
        If ``enable_verb`` is not called, only noun synonyms are returned.

        Args:
            word (str): keyword
            group_ids (list[int]): synonym group IDs

        Returns:
            list[str]: a list of synonym head words
        """
        for dictionary in self._dictionaries:
            gids = dictionary.lookup(word, group_ids)
            if len(gids) == 0:
                continue

            synonyms = []
            for gid in gids:
                ret = self.gather_head_word(word, gid, dictionary)
                if ret:
                    synonyms += ret
            return synonyms

        return []

    def gather_head_word(self, word, group_id, dictionary):
        """Searches synonyms by the ``group_id`` from the ``dictionary``.

        Args:
            word (str): keyword
            group_id (int): synonym group ID
            dictionary (Dictionary): a synonym dictionary

        Returns:
            list[str] | None: head words of synonyms.

                If synonyms with the specified group ID exist in a dictionary, head words of the synonyms are returned.

                Returns ``None`` in the following cases:
                    1. The synonym group with the ``group_id`` does not exist in the ``dictionary``.
                    2. The ``key`` is ambiguous, which is not a trigger of synonym expansion.

        Raises:
            ValueError: The ``group_id`` is defined in the dictionary, but the ``key`` does not exist in the group.
        """
        head_words = []

        synonym_group = dictionary.get_synonym_group(group_id)
        if synonym_group is None:
            return None

        looked_up = synonym_group.lookup(word)
        if looked_up is None:
            raise ValueError(
                "The dictionary (``{}``) has a group ID of {}, "
                "but the key (``{}``) dose not exist in the group.".format(dictionary.filename, group_id, word)
            )
        if looked_up.has_ambiguity:
            return None

        for synonym in synonym_group.get_synonyms():
            if synonym.head_word == word:
                continue
            if not self._can_search_verb and not synonym.is_noun:
                continue

            head_words.append(synonym.head_word)
        return head_words
