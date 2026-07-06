# Can __new__() return an object of another class? Yes

class A:
    pass

class B:
    def __new__(cls):
        return A()

obj = B()

print(type(obj)) #<class '__main__.A'>


# -------
# Can __init__() return something? No. It must return None.

class Test:
    def __init__(self):
        return 10 
obj = Test()
print(obj)

# TypeError: __init__() should return None, not 'int'