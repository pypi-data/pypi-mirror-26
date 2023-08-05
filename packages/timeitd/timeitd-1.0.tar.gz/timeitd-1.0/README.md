# timeitd
A timeit decorator which makes benchmark scripts easy

## Installation
```
$ pip install timeitd
```

## Example
```python
# bench_myfunction.py
from timeitd import timeit
from some_module import myfunction

@timeit(number=10000, unit="ns")
def bench_myfunction():
    v = do_something()
    myfunction(v)
```

Output of this benchmark script is:
```
bench_myfunction execution avg: 1100.312300004589 ns
```

Dependent on `timeit` module.
Time unit is available for ms, us and ns.
