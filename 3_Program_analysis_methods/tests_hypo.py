from operator import add 

def bad_add(a,b):
    print(a,b)
    if (b<-500):
        return -1
    else:
        return add(a,b)

from hypothesis import given, example, settings
from hypothesis.strategies import integers

# Example of a test that should pass every time
@given(a=integers(), b=integers())
def test_addition(a,b):
    assert add(a,b) == a+b

# Example of bad addition and catching it
@given(a=integers(), b=integers())
def test_bad_addition(a,b):
    assert bad_add(a,b) == a+b

# Example where we show how to record existing
# bad examples for next time
# @given(a=integers(), b=integers())
# @example(0,501)
# @settings(max_examples=50)
# def test_bad_addition(a,b):
#     assert bad_add(a,b) == a+b

# Example to show how to limit the ranges
# @given(a=integers(min_value=-500,max_value=500), 
#        b=integers(min_value=-500,max_value=500))
# def test_bad_addition(a,b):
#     assert bad_add(a,b) == a+b

# Example demonstrating different types
# from hypothesis.strategies import floats
# @given(a=floats(min_value=-500,max_value=500), 
#        b=integers(min_value=-500,max_value=500))
# def test_bad_addition(a,b):
#     assert bad_add(a,b) == a+b
