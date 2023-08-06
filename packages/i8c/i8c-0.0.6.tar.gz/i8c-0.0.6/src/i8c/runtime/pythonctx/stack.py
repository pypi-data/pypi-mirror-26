# -*- coding: utf-8 -*-
# Copyright (C) 2015-17 Red Hat, Inc.
# This file is part of the Infinity Note Execution Environment.
#
# The Infinity Note Execution Environment is free software; you can
# redistribute it and/or modify it under the terms of the GNU Lesser
# General Public License as published by the Free Software Foundation;
# either version 2.1 of the License, or (at your option) any later
# version.
#
# The Infinity Note Execution Environment is distributed in the hope
# that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with the Infinity Note Execution Environment; if not,
# see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ...compat import fprint, integer
from .. import memory
from . import functions
from . import types

# XXX most every assert here should be a proper error

class Stack(object):
    def __init__(self, ctx):
        self.ctx = ctx
        self.slots = []

    # Generic push and pop

    def pop_multi_onto(self, types, other):
        """Transfer values from one stack to another."""
        types = list(types)
        other.push_multi(types, self.pop_multi(types))

    def push_multi(self, types, values):
        types, values = map(list, (types, values))
        assert len(types) == len(values)
        typedvalues = list(zip(types, values))
        typedvalues.reverse()
        for type, value in typedvalues:
            self.push_typed(type, value)

    def pop_multi(self, types):
        result = []
        for type in types:
            result.append(self.pop_typed(type))
        return result

    def push_typed(self, type, value):
        assert type is not None
        self.push_boxed(self.__box(type, value))

    def pop_typed(self, type):
        assert type is not None
        return self.__unbox(type, self.pop_boxed())

    def push_boxed(self, boxed_value):
        assert not isinstance(boxed_value, integer)
        self.slots.insert(0, boxed_value)

    def pop_boxed(self):
        return self.slots.pop(0)

    # Push and pop shortcuts

    def push_intptr(self, value):
        self.push_typed(types.IntPtrType, value)

    def pop_unsigned(self):
        return self.pop_typed(types.IntPtrType)

    def pop_signed(self):
        return self.ctx.to_signed(self.pop_unsigned())

    def pop_function(self):
        return self.__unbox_FUNCTION(None, self.pop_boxed())

    # Boxing and unboxing

    def __box(self, type, value):
        return getattr(
            self, "_Stack__box_" + type.name.upper())(type, value)

    def __unbox(self, type, value):
        return getattr(
            self, "_Stack__unbox_" + type.name.upper())(type, value)

    def __box_INTPTR(self, type, value):
        if isinstance(value, memory.Block):
            value = value.location
        assert isinstance(value, integer)
        return self.ctx.uint_t(value)

    def __unbox_INTPTR(self, type, boxed):
        assert isinstance(boxed, self.ctx.uint_t)
        return boxed.value

    def __box_FUNCTION(self, type, value):
        if not isinstance(value, functions.Function):
            # Replace signatures (strings) and UserFunction objects
            # with registered functions.  This is persistent (in
            # that unboxing won't remove it), meaning what you pop
            # (in this case) won't be exactly what you pushed.
            value = self.ctx.get_function(value)
        assert value.type == type
        return value

    def __unbox_FUNCTION(self, type, boxed):
        assert isinstance(boxed, functions.Function)
        assert type is None or boxed.type == type
        return boxed

    def __box_OPAQUE(self, type, value):
        return Opaque(value)

    def __unbox_OPAQUE(self, type, boxed):
        assert isinstance(boxed, Opaque)
        return boxed.value

    # Tracing

    def trace(self):
        return [self.__unbox_unchecked(boxed) for boxed in self.slots]

    def __unbox_unchecked(self, boxed):
        if isinstance(boxed, self.ctx.uint_t):
            return boxed.value
        else:
            return id(boxed)

class Opaque(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "OPAQUE [0x%x]" % id(self)
