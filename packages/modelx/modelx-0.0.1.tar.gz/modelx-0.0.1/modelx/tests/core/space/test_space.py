from textwrap import dedent

import pytest

from modelx.core.api import *
from ..data import testmodule

@pytest.fixture
def samplespace():

    space = new_model(name='samplemodel').new_space(name='samplespace')

    @defcells(space)
    def foo(x):
        if x == 0:
            return 123
        else:
            return foo(x - 1)

    return space


def test_create(samplespace):
    assert samplespace in cur_model().spaces.values()


def test_get_cells_by_cells(samplespace):
    assert samplespace.cells["foo"][10] == 123


def test_get_cells_by_getattr(samplespace):
    assert samplespace.foo[10] == 123


def test_new_cells_from_module(samplespace):


    cells = samplespace.new_cells_from_module(testmodule)
    assert set(testmodule.funcs) == set(cells.keys())


def test_new_cells_from_modulename(samplespace):

    names = __name__.split('.')
    names = names[:-2] + ['data', 'testmodule']
    module_name = '.'.join(names)

    cells = samplespace.new_cells_from_module(module_name)
    assert set(testmodule.funcs) == set(cells.keys())


def test_derived_spaces(samplespace):

    model = cur_model()

    space_a = model.new_space()

    @defcells
    def cells_a(x):
        if x == 0:
            return 1
        else:
            return cells_a(x - 1)

    space_b = model.new_space(bases=space_a)

    space_b.cells_a[0] = 2

    assert space_a.cells_a[2] == 1 and space_b.cells_a(2) == 2


def test_paramfunc(samplespace):

    model = cur_model()
    base = model.new_space(paramfunc=lambda x, y: {'bases': get_self()})

    distance_def = dedent("""\
    def distance():
        return (x ** 2 + y ** 2) ** 0.5
    """)

    base.new_cells(func=distance_def)

    assert base[3, 4].distance == 5


def test_dynamic_spaces(samplespace):

    model = cur_model()
    space = model.new_space(paramfunc=lambda n: {'bases': get_self()})

    @defcells
    def foo(x):
        return x * n

    assert space[1].foo(2) == 2 \
        and space[2].foo(4) == 8


def test_ref(samplespace):

    space = new_space()

    @defcells
    def foo(x):
        return x * n

    space.n = 3
    assert foo(2) == 6


def test_del_cells(samplespace):

    space = new_space()

    @defcells
    def foo(x):
        return 2 * x

    foo(3)
    del space.foo

    with pytest.raises(KeyError):
        space.foo(3)

    with pytest.raises(RuntimeError):
        foo(3)

# ----- Testing _impl  ----

def test_mro_root(samplespace):
    space = cur_space()
    assert [space._impl] == space._impl.mro


def test_fullname(samplespace):
    assert samplespace._impl.get_fullname() == "samplemodel.samplespace"


def test_fullname_omit_model(samplespace):
    assert samplespace._impl.get_fullname(omit_model=True) == 'samplespace'