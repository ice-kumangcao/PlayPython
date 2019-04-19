"""
Python基础学习Demo
"""


# Python基础类型存储
def test_base_id():
    a = 1
    b = 1
    print(id(1), id(b))

    a = 'a'
    b = 'a'
    print(id(a), id(b))

    a = [1, 2, 3]
    b = [1, 2, 3]
    print(id(a) == id(b))


test_base_id()

a = [1, 2, 3]
b = [1, 2, 3]
print(id(a) == id(b))
