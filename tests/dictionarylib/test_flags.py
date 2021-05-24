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

from unittest import TestCase

from chikkarpy.dictionarylib.flags import Flags
from chikkarpy.dictionarylib.format import Acronym, Form, Variant


class TestFlags(TestCase):

    def test_all_zero(self):
        flags = Flags(False, False, Form.NONE, Form.NONE, Form.NONE)
        code = flags.encode()
        new_flags = Flags.from_int(code)
        self.assertFalse(new_flags.has_ambiguity)
        self.assertFalse(new_flags.is_noun)
        self.assertEqual(new_flags.form_type, Form.NONE)
        self.assertEqual(new_flags.acronym_type, Form.NONE)
        self.assertEqual(new_flags.variant_type, Form.NONE)

    def test_max(self):
        flags = Flags(True, True, Form.MISNOMER, Acronym.OTHERS, Variant.MISSPELLED)
        code = flags.encode()
        new_flags = Flags.from_int(code)
        self.assertTrue(new_flags.has_ambiguity)
        self.assertTrue(new_flags.is_noun)
        self.assertEqual(new_flags.form_type, Form.MISNOMER)
        self.assertEqual(new_flags.acronym_type, Acronym.OTHERS)
        self.assertEqual(new_flags.variant_type, Variant.MISSPELLED)
