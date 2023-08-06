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

class FunctionTestCase(object):
    def test_context(self):
        """Test Function.context."""
        self.assertIs(self.func.context, self.ctx)

    def test_is_persistent(self):
        """Test Function.is_persistent."""
        del self.ctx
        self._test_persistence("func")

    def test_ref(self):
        """Test Function.ref."""
        ref = self.func.ref
        self.assertIsInstance(ref, libi8x.FunctionReference)

    def test_signature(self):
        """Test Function.signature."""
        sig = self.func.signature
        self.assertEqual(sig, self.signature)

    def test_relocations(self):
        """Test Function.relocations."""
        relocs = self.func.relocations
        self.assertIsSequence(relocs)

    def test_unregister(self):
        """Test Function.unregister."""
        self.assertEqual(len(self.ctx.functions), 1)
        self.func.unregister()
        self.assertEqual(len(self.ctx.functions), 0)

class TestBytecodeFunction(TestCase, FunctionTestCase):
    def setUp(self):
        self.ctx = self.ctx_new()
        self.func = self.ctx.import_bytecode(self.GOOD_NOTE)
        self.signature = "example::factorial(i)i"

    def test_note(self):
        """Test Function.note."""
        note = self.func.note
        self.assertIsInstance(note, libi8x.Note)

class TestNativeFunction(TestCase, FunctionTestCase):
    def setUp(self):
        self.ctx = self.ctx_new()
        self.signature = "test::func()"
        self.func = self.ctx.import_native(self.signature,
                                           self.do_not_call)

    def test_note(self):
        """Test Function.note."""
        note = self.func.note
        self.assertIsNone(note)
