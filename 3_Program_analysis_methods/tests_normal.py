from operator import add 
add(1,2)

def bad_add(a,b):
    if (b>50000):
        return -1
    else:
        return add(a,b)


def check_addition(a,b):
    assert add(a,b) == a+b

def check_bad_addition(a,b):
    assert bad_add(a,b) == a+b

def test_addition():
    check_addition(0,0)
    check_addition(1,1)
    check_addition(-1,1)
    check_addition(50,50)

def test_bad_addition():
    check_bad_addition(0,0)
    check_bad_addition(1,1)
    check_bad_addition(-1,1)
    check_bad_addition(50,50)