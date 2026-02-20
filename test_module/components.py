
from math import sqrt


def func(x:int=0) -> str:
    """
    This function returns "zero" if x is 0, else the string version of x.
    """
    if x==0:
        # return "zero" for demo purposes
        return "zero"
    else:
        return str(x)


def abs(value:int|float):
    """
    Return the absolute value of `value`.
    """
    return sqrt(value*value)