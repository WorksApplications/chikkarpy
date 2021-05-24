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

from .dictionarylib.flags import Flags


class Synonym(object):
    """
    A synonym
    """
    def __init__(self, head_word, lexeme_ids, flags, category):
        """Construct a new synonym with the specified parameter.

        Args:
            head_word (str): a notation string
            lexeme_ids (list[int]): IDs of lexeme in the synonym group
            flags (Flags): encoded flags
            category (str): category Information of the synonym
        """
        self._head_word = head_word
        self._lexeme_ids = lexeme_ids
        self._flags = flags
        self._category = category

    @property
    def head_word(self):
        """str: the notation of this synonym"""
        return self._head_word

    @property
    def lexeme_ids(self):
        """list[int]: the IDs of the lexemes that corresponds to this synonym"""
        return self._lexeme_ids

    @property
    def category(self):
        """str: the category information of this synonym"""
        return self._category

    @property
    def flags(self):
        """Flags: encoded flags"""
        return self._flags

    @property
    def has_ambiguity(self):
        """bool: ``True`` if this synonym is ambiguous, ``False`` otherwise"""
        return self._flags.has_ambiguity

    @property
    def is_noun(self):
        """bool: ``True`` if this synonym is a noun, ``False`` otherwise"""
        return self._flags.is_noun

    @property
    def form_type(self):
        """int: the word form type of this synonym"""
        return self._flags.form_type

    @property
    def acronym_type(self):
        """int: the acronym type of this synonym"""
        return self._flags.acronym_type

    @property
    def variant_type(self):
        """int: the variant type of this synonym"""
        return self._flags.variant_type
