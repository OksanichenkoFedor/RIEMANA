import numpy as np
from numba import njit, f8
from numba.experimental import structref

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
    def __new__(cls, x, y):
        self = my_class_constructor(x, y)
        return self

    @property
    def x(self):
        return get_x(self)

    @property
    def y(self):
        return get_y(self)

    @x.setter
    def x(self, x):
        set_x(self, x)

    @y.setter
    def y(self, y):
        set_y(self, y)



# Create a type for the class and define Numba-to-Python interfacing (boxing)
MyClassTemplate = create_type_template(MyClass)
MyType = MyClassTemplate([("x", f8[:]), ("y", f8[:])])
structref.define_boxing(MyClassTemplate, MyClass)

# Define the typed constructor implementation
@njit(MyType(f8[:], f8[:]), cache=True)
def my_class_constructor(x, y):
    self = structref.new(MyType)
    self.x = x
    self.y = y
    return self

# Implementations of getters/setters/methods
@njit()
def get_x(self):
    return self.x


@njit()
def get_y(self):
    return self.y

@njit()
def set_x(self, x):
    self.x = x

@njit()
def set_y(self, y):
    self.y = y

my_instance = MyClass(np.array([1.0, 2.0, 3.0]), np.array([3.0, 3.0, 3.0]))

print(my_instance.x)
my_instance.x = np.array([2.0, 2.0, 3.0])
print(my_instance.x)

print(my_instance.y)
my_instance.y = np.array([3.0, 2.0, 3.0])
print(my_instance.y)