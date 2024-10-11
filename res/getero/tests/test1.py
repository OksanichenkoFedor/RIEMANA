import numpy as np
from numba.pycc import CC
from numba import njit, f8
from numba.experimental import structref
from numba.core.extending import overload_method, overload

# This is boilerplate that can be imported from elsewhere and re-used
def create_type_template(cls):
    source = f"""
from numba.core import types
from numba.experimental import structref
@structref.register
class {cls.__name__}Type(types.StructRef):
    pass
"""
    glbs = globals()
    exec(source, glbs)

    return glbs[f"{cls.__name__}Type"]

# Create a Python class that will be a proxy for the Numba class - the actual
# implementation is not defined here.
class MyClass(structref.StructRefProxy):
    def __new__(cls, x):
        self = my_class_constructor(x)
        return self

    @property
    def x(self):
        return _x(self)

    @property
    def y(self):
        return _y(self)

    def acc(self, a=1):
        return _acc(self, a)


# Create a type for the class and define Numba-to-Python interfacing (boxing)
MyClassTemplate = create_type_template(MyClass)
MyType = MyClassTemplate([("x", f8[:]), ("y", f8[:])])
structref.define_boxing(MyClassTemplate, MyClass)

# Define the typed constructor implementation
@njit(MyType(f8[:]), cache=True)
def my_class_constructor(x):
    self = structref.new(MyType)
    self.x = x
    self.y = 2 * x
    return self


# Overload the Python constructor with our Numba implementation
@overload(MyClass)
def overload_MyClass(x):
    def implementation(x):
        return my_class_constructor(x)

    return implementation


# Implementations of getters/setters/methods
@njit(cache=True)
def _x(self):
    return self.x


@njit(cache=True)
def _y(self):
    return self.y


@njit(cache=True)
def _acc(self, a=1):
    return self.x.sum() + a + self.y


# Extra step required for methods to expose in jit-code
@njit(cache=True)
@overload_method(MyClassTemplate, "acc")
def overload_acc(self, a=1):
    python_implementation = _acc.py_func
    return python_implementation


# Test:
# running this script prints
# [12. 14. 16.]
# [2. 4. 6.]
# [1. 2. 3.]
# [11. 13. 15.]
# [12. 14. 16.]
# [2. 4. 6.]
# [1. 2. 3.]
# [11. 13. 15.]
# AOT compiling
# [12. 14. 16.]
if __name__ == "__main__":

    # Create a function that operates on an instance of our new class and
    # ahead-of-time (AOT) and JIT compile it
    cc = CC("my_module")

    @njit(f8[:](MyType), cache=True)
    @cc.export("add", f8[:](MyType))
    def add(instance):
        return instance.acc(4)

    # Create a an instance of MyClass and test it in Python
    my_instance = MyClass(np.array([1.0, 2.0, 3.0]))
    print(add(my_instance))
    print(my_instance.y)
    print(my_instance.x)
    print(my_instance.acc(3))

    # Test in jit-code
    @njit(cache=True)
    def test_jit_code():
        my_instance = MyClass(np.array([1.0, 2.0, 3.0]))
        print(add(my_instance))
        print(my_instance.y)
        print(my_instance.x)
        print(my_instance.acc(3))

    test_jit_code()

    # Test it in AOT code
    print("AOT compiling")
    cc.compile()

    def test_aot_code():
        import my_module

        print(my_module.add(my_instance))

    test_aot_code()