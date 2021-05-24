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

class Flags:
    def __init__(self, has_ambiguity, is_noun, form_type, acronym_type, variant_type):
        """Constructs flags of a synonym.

        Args:
            has_ambiguity (bool): ``True`` if a synonym is ambiguous, ``False`` otherwise
            is_noun (bool): ``True`` if a synonym is a noun, ``False`` otherwise
            form_type (int): a word form type of a synonym
            acronym_type (int): an acronym type of a synonym
            variant_type (int): a variant type of a synonym
        """
        self._has_ambiguity = has_ambiguity
        self._is_noun = is_noun
        self._form_type = form_type
        self._acronym_type = acronym_type
        self._variant_type = variant_type

    @classmethod
    def from_int(cls, flags):
        """Reads and returns flags from the specified int value.

        Args:
            flags (int): int-type flag

        Returns:
            Flags: a flags of a synonym
        """
        has_ambiguity = ((flags & 0x0001) == 1)
        is_noun = ((flags & 0x0002) == 2)
        form_type = (flags >> 2) & 0x0007
        acronym_type = (flags >> 5) & 0x0003
        variant_type = (flags >> 7) & 0x0003
        return cls(has_ambiguity, is_noun, form_type, acronym_type, variant_type)

    @property
    def has_ambiguity(self):
        """bool: ``True`` if a synonym is ambiguous, ``False`` otherwise"""
        return self._has_ambiguity

    @property
    def is_noun(self):
        """bool: ``True`` if a synonym is a noun, ``False`` otherwise"""
        return self._is_noun

    @property
    def form_type(self):
        """int: a word form type of a synonym"""
        return self._form_type

    @property
    def acronym_type(self):
        """int: an acronym type of a synonym"""
        return self._acronym_type

    @property
    def variant_type(self):
        """int: a variant type of a synonym"""
        return self._variant_type

    def encode(self):
        """Encodes this ``Flags`` object.

        Returns:
            int: encoded flags
        """
        flags = 0
        flags |= 1 if self.has_ambiguity else 0
        flags |= (1 if self.is_noun else 0) << 1
        flags |= self.form_type << 2
        flags |= self.acronym_type << 5
        flags |= self.variant_type << 7
        return flags
