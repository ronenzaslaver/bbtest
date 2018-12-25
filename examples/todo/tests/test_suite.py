""" How to test a todo?

This Module includes the test suite that verifies the todo component using
a black box methodology.

"""
import bbtest

from . import ToDoBox


class ToDoTest(bbtest.BBTestCase):

    LAB = {
        'host1': {
            'class': bbtest.LocalHost,
            'boxes': [ToDoBox],
         },
    }

    def test_add(self):
        box = self.lab.boxes[ToDoBox.NAME][0]
        box.add("Foo")
        todos = box.list()
        self.assertEqual(todos, ["Foo"])
