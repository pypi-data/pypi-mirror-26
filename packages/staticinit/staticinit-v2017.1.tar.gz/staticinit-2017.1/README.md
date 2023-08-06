static-init
===========

The module [staticinit](staticinit.py) defines the decorator `@staticinit.init()` for classes, which executes a static
constructor after the annotated class has been created.
By default, the name of the according constructor method is assumed to be `__static_init__`, but an alternative name may
be specified via the keyword arg `init_meth`. 
Notice further that the constructor has to be a class method.

The following example illustrates how to use this module: 
```python
import staticinit

@staticinit.init()
class SomeClass(object):

    @classmethod
    def __static_init__(cls):
        # do some initialization stuff here...
```
