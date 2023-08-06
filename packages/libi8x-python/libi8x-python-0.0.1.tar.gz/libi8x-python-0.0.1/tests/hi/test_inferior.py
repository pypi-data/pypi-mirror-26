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
import struct
import sys

class TestInferior(TestCase):
    def test_context(self):
        """Test Inferior.context."""
        ctx = self.ctx_new()
        inf = ctx.new_inferior()
        self.assertIs(inf.context, ctx)

    def test_is_persistent(self):
        """Test Inferior.is_persistent."""
        self.inf = self.ctx_new().new_inferior()
        self._test_persistence("inf")

class ReadMemRelocTestCase(TestCase):
    def _do_readmem_reloc_test(self, inf):
        ctx = inf.context
        func = ctx.import_bytecode(self.TESTNOTE).ref
        xctx = ctx.new_xctx()
        result = xctx.call(func, inf, *self.TESTNOTE_ARGS)
        self.assertEqual(result, self.TESTNOTE_EXPECT_RESULT)

class TestInferiorReadMemory(ReadMemRelocTestCase):
    TESTNOTE = ReadMemRelocTestCase.DEREF_NOTE
    INFERIOR_MEMORY = b"HeLlOmUmXoXoX"
    TESTNOTE_ARGS = (1,)
    TESTNOTE_EXPECT_RESULT = struct.unpack(b"<I", b"eLlO")

    def test_no_readmem_func(self):
        """Test reading memory with no memory reader function set."""
        ctx = self.ctx_new()
        inf = ctx.new_inferior()
        self.assertRaises(NotImplementedError,
                          self._do_readmem_reloc_test, inf)

    def test_readmem_func_in_object(self):
        """Test reading memory with the function set in the object."""
        ctx = self.ctx_new()
        inf = ctx.new_inferior()
        inf._test_memory = self.INFERIOR_MEMORY
        def testfunc(inf, addr, len):
            return inf._test_memory[addr:addr + len]
        inf.read_memory = testfunc
        self._do_readmem_reloc_test(inf)

    def test_readmem_func_in_class(self):
        """Test reading memory with the function set in the class."""
        expect_result = self.TESTNOTE_EXPECT_RESULT
        class Inferior(libi8x.Inferior):
            _test_memory = self.INFERIOR_MEMORY
            def read_memory(self, addr, len):
                return self._test_memory[addr:addr + len]
        class Context(libi8x.Context):
            INFERIOR_CLASS = Inferior
        ctx = self.ctx_new(klass=Context)
        self._do_readmem_reloc_test(ctx.new_inferior())

class TestInferiorRelocation(ReadMemRelocTestCase):
    TESTNOTE = ReadMemRelocTestCase.RELOC_NOTE
    TESTNOTE_ARGS = ()
    TESTNOTE_EXPECT_RESULT = \
        (((sys.maxsize << 1) | 1) & 0x9192939495969798,)

    def test_no_reloc_func(self):
        """Test relocation with no relocation function set."""
        ctx = self.ctx_new()
        inf = ctx.new_inferior()
        self.assertRaises(NotImplementedError,
                          self._do_readmem_reloc_test, inf)

    def test_reloc_func_in_object(self):
        """Test relocation with the function set in the object."""
        ctx = self.ctx_new()
        inf = ctx.new_inferior()
        inf._expect_result = self.TESTNOTE_EXPECT_RESULT[0]
        def testfunc(inf, reloc):
            return inf._expect_result
        inf.relocate_address = testfunc
        self._do_readmem_reloc_test(inf)

    def test_reloc_func_in_class(self):
        """Test relocation with the function set in the class."""
        expect_result = self.TESTNOTE_EXPECT_RESULT
        class Inferior(libi8x.Inferior):
            _expect_result = self.TESTNOTE_EXPECT_RESULT[0]
            def relocate_address(self, reloc):
                return self._expect_result
        class Context(libi8x.Context):
            INFERIOR_CLASS = Inferior
        ctx = self.ctx_new(klass=Context)
        self._do_readmem_reloc_test(ctx.new_inferior())
