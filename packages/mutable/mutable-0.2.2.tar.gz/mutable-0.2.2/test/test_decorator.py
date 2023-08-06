import unittest
import json

from mutable import mutable

class TestDecorator(unittest.TestCase):

    def test_decorator(self):

        @mutable
        class MyMutable:
            def __init__(self):
                self.a = 1

        # Test prop access
        o = MyMutable({'a': 2, 'b': 'test'})
        self.assertEqual(o.a, 2)
        self.assertEqual(o.b, 'test')

        # Test prop assignment
        o.a = {"c": {"d": 3}}
        self.assertEqual(o.a.c.d, 3)

    def test_decorator_empty(self):

        @mutable
        class MyMutable:
            def __init__(self):
                self.a = 1

        # Test prop access
        o = MyMutable()
        self.assertEqual(o.a, 1)

        # Test prop assignment
        o.a = {"c": {"d": 2}}
        self.assertEqual(o.a.c.d, 2)

    def test_decorator_with_args(self):

        @mutable
        class MyMutable:
            def __init__(self, c):
                self.a = 1
                self.c = c

        o = MyMutable({'a': 2, 'b': 'test'}, 10)

        # Test prop access
        self.assertEqual(o.a, 2)
        self.assertEqual(o.b, 'test')
        self.assertEqual(o.c, 10)

        # Test prop assignment
        o.c = {"a": {"b": 3}}
        self.assertEqual(o.c.a.b, 3)

    def test_decorator_with_kwargs(self):

        @mutable
        class MyMutable:
            def __init__(self, c=None):
                self.a = 1
                self.c = c

        o = MyMutable({'a': 2, 'b': 'test'}, c=10)

        self.assertEqual(o.a, 2)
        self.assertEqual(o.b, 'test')
        self.assertEqual(o.c, 10)

    def test_decorator_mixed1(self):

        @mutable
        class MyMutable:
            def __init__(self, c, d, e=None, f=None):
                self.a = 1
                self.c = c
                self.d = d
                self.e = e
                self.f = f

        o = MyMutable({'a': 2, 'b': 'test'}, 10, 11, e='test')

        self.assertEqual(o.a, 2)
        self.assertEqual(o.b, 'test')
        self.assertEqual(o.c, 10)
        self.assertEqual(o.d, 11)
        self.assertEqual(o.e, 'test')
        self.assertEqual(o.f, None)
        self.assertEqual(o.__class__.__name__, 'MyMutable')

    def test_decorator_func_collision(self):

        @mutable
        class MyMutable:
            def __init__(self):
                self.a = 1
            def args(self):
                return 0
            def save(self):
                return 1
            def load(self):
                return 2
            def fields(self):
                return 3
            def props(self):
                return 4

        # Test prop access
        o = MyMutable({'a': 2, 'b': 'test'})
        self.assertEqual(o.a, 2)
        self.assertEqual(o.b, 'test')

        # Test prop assignment
        o.a = {"c": {"d": 3}}
        self.assertEqual(o.a.c.d, 3)

        self.assertEqual(o.args(), 0)
        self.assertEqual(o.save(), 1)
        self.assertEqual(o.load(), 2)
        self.assertEqual(o.fields(), 3)
        self.assertEqual(o.props(), 4)

    def test_decorator_mixed2(self):

        @mutable
        class MyMutable:
            def __init__(self, c, d, e=None, f=None):
                self.a = 1
                self.c = c
                self.d = d
                self.e = e
                self.f = f

        o = MyMutable({'a': 2, 'b': 'test'}, 10, 11, e='test', name='MyName')

        self.assertEqual(o.a, 2)
        self.assertEqual(o.b, 'test')
        self.assertEqual(o.c, 10)
        self.assertEqual(o.d, 11)
        self.assertEqual(o.e, 'test')
        self.assertEqual(o.f, None)
        self.assertEqual(o.__class__.__name__, 'MyName')

if __name__ == '__main__':
    unittest.main()
