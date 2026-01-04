def improve(update, close, target, guess = 1):
    while not close(guess, target):
        guess = update(guess, target)
    return guess

# def golden_update(guess):
#     return 1/guess + 1

def sqrt_close_to_successor(guess, target):
    return approx_eq(guess * guess, target)

def approx_eq(x, y, tolerance=1e-14):
    return abs(x - y) < tolerance

def sqrt_update(x, a):
    return (x + a / x) / 2

from math import sqrt
x = 15
print(improve(sqrt_update, sqrt_close_to_successor, x), sqrt(x))