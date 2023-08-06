# -*- coding: utf-8 -*-
# Copyright (C) 2017 Red Hat, Inc.
# This file is part of the Infinity Note Execution Library.
#
# The Infinity Note Execution Library is free software; you can
# redistribute it and/or modify it under the terms of the GNU Lesser
# General Public License as published by the Free Software
# Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# The Infinity Note Execution Library is distributed in the hope
# that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with the Infinity Note Execution Library; if not,
# see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from . import *

class TestRelocation(TestCase):
    IMPORT_NAME = r"C:\Some\File\Or another"
    EXPECT_NAME = IMPORT_NAME

    IMPORT_OFFSET = 23
    EXPECT_OFFSET = IMPORT_OFFSET + 10

    def setUp(self):
        self.ctx = self.ctx_new()
        self.func = self.ctx.import_bytecode(self.RELOC_NOTE,
                                             srcname=self.IMPORT_NAME,
                                             srcoffset=self.IMPORT_OFFSET)
        self.reloc = list(self.func.relocations)[0]

    def test_context(self):
        """Test Relocation.context."""
        self.assertIs(self.reloc.context, self.ctx)

    def test_is_persistent(self):
        """Test Relocation.is_persistent."""
        del self.ctx, self.func
        self._test_persistence("reloc")

    def test_function(self):
        """Test Relocation.function."""
        self.assertIs(self.reloc.function, self.func)

    def test_srcname(self):
        """Test Relocation.srcname."""
        self.assertEqual(self.reloc.srcname, self.EXPECT_NAME)

    def test_srcoffset(self):
        """Test Relocation.srcoffset."""
        self.assertEqual(self.reloc.srcoffset, self.EXPECT_OFFSET)

    def test_no_srcoffset(self):
        """Test Relocation.srcoffset returning None."""
        self.func = self.ctx.import_bytecode(self.RELOC_NOTE)
        self.reloc = list(self.func.relocations)[0]
        self.assertIsNone(self.reloc.srcoffset)
