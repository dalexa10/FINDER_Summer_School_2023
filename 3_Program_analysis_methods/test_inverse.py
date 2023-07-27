from hypothesis import given
from hypothesis.strategies import integers, floats

def check_inverse(f,x):
    assert f(f(x)) == x

@given(x = floats(allow_nan=False))
def test_negx(x):
    f = lambda a: -a
    check_inverse(f,x)

@given(x = floats(allow_nan=False))
def test_1x(x):
    f = lambda a: 1/x
    check_inverse(f,x)

@given(x = floats(allow_nan=False))
def test_3(x):
    f = lambda a: a/(a-1)
    check_inverse(f,x)
