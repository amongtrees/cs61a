def count_frames(f):
    def counted(n):
        counted.call += 1
        # counted.max_count = max(counted.max_count, counted.open_count)
        # result = f(n)
        # counted.open_count -= 1
        return f(n)
    # counted.open_count = 0
    # counted.max_count = 0
    counted.call = 0
    return counted

def memo(f):
    cache = {}
    def memorized(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    return memorized

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 2) + fib(n - 1)

fib = count_frames(fib)
fib(6)
print(fib.call)
fib_counted = count_frames(fib)
fib =memo(fib_counted)
fib(6)
print(fib_counted.call)
pass