# Copyright (c) 2017 Fumito Hamamura <fumito.ham@gmail.com>

# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation version 3.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.

from types import FunctionType
from textwrap import dedent
from collections import Sequence
from collections.abc import (
    Container,
    Callable,
    Sized)

from modelx.core.base import (
    ObjectArgs,
    Impl,
    Interface)
from modelx.core.formula import (
    Formula,
    create_closure,
    NULL_FORMULA)
from modelx.core.util import is_valid_name
from modelx.core.errors import NoneReturnedError


class CellArgs(ObjectArgs):

    state_attrs = ['cells'] + ObjectArgs.state_attrs

    def __init__(self, cells, args, kwargs=None):

        if isinstance(args, Sequence):
            args = tuple(arg._impl.single_value
                         if isinstance(arg, Cells) else arg for arg in args)

        elif isinstance(args, Cells):
            args = args._impl.single_value

        if kwargs is not None:
            for key, arg in kwargs.items():
                if isinstance(arg, Cells):
                    kwargs[key] = arg._impl.single_value

        ObjectArgs.__init__(self, cells, args, kwargs)
        self.cells = self.obj_

    def eval_formula(self):

        func = self.cells.formula.func
        codeobj = func.__code__
        name = self.cells.name   # func.__name__
        namespace = self.cells.space.namespace

        closure = func.__closure__  # None normally.
        if closure is not None:     # pytest fails without this.
            closure = create_closure(self.cells.interface)

        altfunc = FunctionType(codeobj, namespace,
                               name=name, closure=closure)

        return altfunc(**self.arguments)


class CellsMaker:

    def __init__(self, *, space, name):
        self.space = space  # SpaceImpl
        self.name = name

    def __call__(self, func):
        return self.space.new_cells(func=func,
                                       name=self.name).interface


class CellsImpl(Impl):
    """
    Data container optionally with a formula to set its own values.

    **Creation**

    **Deletion**

    * Values dependent on the cell are deleted clear_all()
    * Values dependent on the derived cells of the cells are deleted
    * Derived cells are deleted _del_derived
    * The cells is deleted _del_self

    **Changing formula**
    clear_all
    _set_formula
    _clear_all_derived
    _set_formula_derived

    **Changing can_return_none**

    **Setting Values**
    clear()
    _set

    **Getting Values**

    **Deleting Values**
    clear(params)
    clear_all
    _clear_all_derived()

    Args:
        space: Space to contain the cell.
        name: Cell's name.
        func: Python function or Formula
        data: array-like, dict, pandas.DataSeries or scalar values.
    """

    def __init__(self, *, space, name=None, func=None, data=None):

        Impl.__init__(self, Cells)

        self.system = space.system
        self.model = space.model
        self.space = space
        if func is None:
            self.formula = NULL_FORMULA
        else:
            self.formula = Formula(func)

        self.can_return_none = False

        if is_valid_name(name):
            self.name = name
        elif is_valid_name(self.formula.name):
            self.name = self.formula.name
        else:
            self.name = space.cellsnamer.get_next(space.namespace)

        self.data = {}
        if data is None:
            data = {}
        self.data.update(data)

    def del_self(self):
        """Delete content of self. Called from NullImpl(self)"""
        self.clear_all_values()

    # ----------------------------------------------------------------------
    # Serialization by pickle

    state_attrs = ['model',
                   'space',
                   'formula',
                   'name',
                   'data',
                   'can_return_none'] + Impl.state_attrs

    def __getstate__(self):
        state = {key: value for key, value in self.__dict__.items()
                 if key in self.state_attrs}

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def restore_state(self, system):
        """Called after unpickling to restore some attributes manually."""
        self.system = system

    def __repr__(self):
        return '<CellsImpl: %s>' % self.name

    def get_fullname(self, omit_model=False):
        return self.space.get_fullname(omit_model) + '.' + self.name

    @property
    def signature(self):
        return self.formula.signature

    @property
    def parameters(self):
        return self.signature.parameters

    @property
    def repr_(self):

        format_ = dedent("""\
        name: %s
        space: %s
        number of cells: %s""")

        return format_ % (self.name,
                          self.space.name,
                          len(self.data))

    def has_cell(self, args):
        return args in self.data

    def is_scalar(self):
        return len(self.parameters) == 0

    @property
    def single_value(self):
        if self.is_scalar():
            return self.get_value(())
        else:
            return TypeError

    @property
    def is_derived(self):
        return self.name in self.space.derived_cells

    def clear_formula(self):
        self.set_formula(NULL_FORMULA)

    def set_formula(self, func):
        if not self.is_derived:
            formula = Formula(func)
            self.model.clear_obj(self)
            self.formula = formula
            self.space.self_cells_set_update()
        else:
            raise NotImplementedError('Cannot change derived cells formula')

    def get_value(self, args, kwargs=None):

        ptr = CellArgs(self, args, kwargs)
        args = ptr.argvalues

        if self.has_cell(args):
            value = self.data[args]

        else:
            self.system.callstack.append(ptr)
            try:
                value = ptr.eval_formula()

                if self.has_cell(args):
                    # Assignment took place inside the cell.
                    if value is not None:
                        raise ValueError("Duplicate assignment for %s"
                                         % args)
                    elif self.data[args] is None and not self.can_return_none:
                        tracemsg = self.system.callstack.tracemessage()
                        raise NoneReturnedError(ptr, tracemsg)
                    else:
                        value = self.data[args]

                elif value is not None:
                    self._store_value(ptr, value, False)

                elif self.can_return_none:
                    self._store_value(ptr, value, False)

                else:
                    tracemsg = self.system.callstack.tracemessage()
                    raise NoneReturnedError(ptr, tracemsg)
            finally:
                self.system.callstack.pop()

        graph = self.model.cellgraph
        if not self.system.callstack.is_empty():
            graph.add_path([ptr, self.system.callstack.last()])
        else:
            graph.add_node(ptr)

        return value

    def set_value(self, key, value):

        ptr = CellArgs(self, key)

        if self.system.callstack.is_empty():
            self._store_value(ptr, value, True)
            self.model.cellgraph.add_node(ptr)
        else:
            if ptr == self.system.callstack.last():
                self._store_value(ptr, value, False)
            else:
                raise KeyError("Assignment in cells other than %s" %
                               ptr.argvalues)

    def clear_value(self, args, **kwargs):

        if not args and not kwargs:
            self.clear_all_values()
        else:
            ptr = CellArgs(self, args, kwargs)
            if self.has_cell(ptr.argvalues):
                self.model.clear_descendants(ptr)

    def clear_all_values(self):
        for args in list(self.data):
            self.clear_value(args)

    def _store_value(self, ptr, value, overwrite=False):

        key = ptr.argvalues

        if not ptr.cells.has_cell(key):
            self.data[key] = value

        elif overwrite:
            self.clear_value(key)
            self.data[key] = value

        else:
            raise ValueError("Value already exists for %s" %
                             ptr.arguments)

    def to_series(self):
        from modelx.io.pandas import cells_to_series

        return cells_to_series(self)

    def to_frame(self):

        from modelx.io.pandas import cells_to_dataframe

        return cells_to_dataframe(self)






class Cells(Interface, Container, Callable, Sized):
    """Data container with a formula to calculate its own values.

    Cells are created by ``new_cells`` method or its variant methods of
    the containing space, or by function definitions with ``defcells``
    decorator.
    """
    # __slots__ = ('_impl',)

    def __contains__(self, args):
        return self._impl.has_cell(args)

    def __getitem__(self, key):
        return self._impl.get_value(key)

    def __call__(self, *args, **kwargs):
        return self._impl.get_value(args, kwargs)

    def __len__(self):
        return len(self._impl.data)

    def __setitem__(self, key, value):
        """Set value of a particular cell"""
        self._impl.set_value(key, value)

    def __iter__(self):

        def inner():
            keys = sorted(tuple(arg for arg in key)
                          for key in self._impl.data.keys())

            for args in keys:
                yield args

        return inner()

    def clear_formula(self):
        """Clear the formula."""
        self._impl.clear_formula()

    def set_formula(self, func):
        """Set the formula."""
        self._impl.set_formula(func)

    def copy(self, space=None, name=None):
        """Make a copy of itself and return it."""
        return Cells(space=space, name=name, func=self.formula)

    def __hash__(self):
        return hash(id(self))

    # def __repr__(self):
    #     return self._impl.repr_

    def clear(self, *args, **kwargs):
        """Clear all the values."""
        return self._impl.clear_value(args, **kwargs)

    # ----------------------------------------------------------------------
    # Coercion to single value

    def __bool__(self):
        """True if self != 0. Called for bool(self)."""
        return self.get_value() != 0

    def __add__(self, other):
        """self + other"""
        return self._impl.single_value + other

    def __radd__(self, other):
        """other + self"""
        return self.__add__(other)

    def __neg__(self):
        """-self"""
        raise -self._impl.single_value

    def __pos__(self):
        """+self"""
        raise +self._impl.single_value

    def __sub__(self, other):
        """self - other"""
        return self + -other

    def __rsub__(self, other):
        """other - self"""
        return -self + other

    def __mul__(self, other):
        """self * other"""
        return self._impl.single_value * other

    def __rmul__(self, other):
        """other * self"""
        return self.__mul__(other)

    def __truediv__(self, other):
        """self / other: Should promote to float when necessary."""
        return self._impl.single_value / other

    def __rtruediv__(self, other):
        """other / self"""
        return other / self._impl.single_value

    def __pow__(self, exponent):
        """self ** exponent
        should promote to float or complex when necessary.
        """
        return self._impl.single_value ** exponent

    def __rpow__(self, base):
        """base ** self"""
        return base ** self._impl.single_value

    def __abs__(self):
        """Returns the Real distance from 0. Called for abs(self)."""
        raise NotImplementedError

    # ----------------------------------------------------------------------
    # Comparison operations

    def __eq__(self, other):
        """self == other"""
        if self._impl.is_scalar():
            return self._impl.single_value == other
        elif isinstance(other, Cells):
            return self is other
        else:
            raise TypeError

    def __lt__(self, other):
        """self < other"""
        return self._impl.single_value < other

    def __le__(self, other):
        """self <= other"""
        return self.__eq__(other) or self.__lt__(other)

    def __gt__(self, other):
        """self > other"""
        return self._impl.single_value > other

    def __ge__(self, other):
        """self >= other"""
        return self.__eq__(other) or self.__gt__(other)

    # ----------------------------------------------------------------------
    # Conversion to Pandas objects

    def to_series(self):
        """Convert the cells itself into a Pandas Series and return it."""
        return self._impl.to_series()

    @property
    def series(self):
        """Alias of ``to_series()``."""
        return self._impl.to_series()

    def to_frame(self):
        """Convert the cells itself into a Pandas DataFrame and return it."""
        return self._impl.to_frame()

    @property
    def frame(self):
        """Alias of ``to_frame()``."""
        return self._impl.to_frame()

    # ----------------------------------------------------------------------
    # Attributes

    @property   # TODO: Test can_return_none
    def can_return_none(self):
        """bool: If True, the cells can return None, otherwise an error
        is raised upon returning None. Defaults to False."""
        return self._impl.can_return_none

    @can_return_none.setter
    def can_return_none(self, value):
        self._impl.can_return_none = bool(value)


    def set_formula(self, func):
        """Set formula from a function."""
        self._impl.set_formula(func)

    def clear_formula(self):
        """Clear the formula."""
        self._impl.clear_formula()
