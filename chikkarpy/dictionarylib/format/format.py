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

from enum import IntEnum


class Column(IntEnum):
    """https://github.com/WorksApplications/SudachiDict/blob/develop/docs/synonyms.md"""
    GROUP_ID = 0
    IS_NOUN = 1
    AMBIGUITY = 2
    LEXEME_IDS = 3
    FORM_TYPE = 4
    ACRONYM_TYPE = 5
    VARIANT_TYPE = 6
    CATEGORY = 7
    HEAD_WORD = 8


class IsNoun(IntEnum):
    TRUE = 1
    FALSE = 2


class Ambiguity(IntEnum):
    FALSE = 0
    TRUE = 1
    INVALID = 2


class Form(IntEnum):
    # Typical form
    NONE = 0
    # Translated from another language
    TRANSLATION = 1
    # Alias or common name
    ALIAS = 2
    # Old name
    OLD_NAME = 3
    # Misused words
    MISNOMER = 4


class Acronym(IntEnum):
    # Typical Abbreviations
    NONE = 0
    # Abbreviations written in Latin letters
    ALPHABET = 1
    # Abbreviations written outside the Latin alphabet
    OTHERS = 2


class Variant(IntEnum):
    # Typical form
    NONE = 0
    # Original spelling of foreign words or romanization of Japanese words
    ALPHABET = 1
    # Variant notation
    GENERAL = 2
    # Misspelled words
    MISSPELLED = 3
