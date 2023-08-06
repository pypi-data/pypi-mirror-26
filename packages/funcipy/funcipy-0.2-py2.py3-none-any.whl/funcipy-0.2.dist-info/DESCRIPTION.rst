funcipy
=======

A library to inject common functional programming operations as methods
into iterable objects. Currently, it supports ``map`` operation.

Getting the library
-------------------

The library can be installed via ``pip install funcipy``. Similarly, it
can be uninstalled via ``pip uninstall funcipy``.

Usage
-----

When you want to inject common functional programming operations as
methods into an object *O*, invoke ``funcipy.funcipy.funcify`` function
with *O* as the argument. If *O* is iterable, then the function will
return an object that

1. provides the same interface as the input object and
2. has functional programming operations as methods.

Otherwise, *O* is returned as is.

Here are few example invocations.

.. code:: python

    from funcipy.funcipy import funcify

    i = range(1, 10)
    print("Map function: " + ' '.join(map(str, i)]))
    tmp1 = funcify(i)
    print("Map function applied to funcified object: " + ' '.join(map(str, tmp1)))
    print("Map method: " + ' '.join(tmp1.map(str)]))
    print("Map method chaining: " + ' '.join(tmp1.map(str).map(lambda x: x * 2)))

Attribution
-----------

Copyright (c) 2017, Venkatesh-Prasad Ranganath

Licensed under BSD 3-clause "New" or "Revised" License
(https://choosealicense.com/licenses/bsd-3-clause/)

**Authors:** Venkatesh-Prasad Ranganath


