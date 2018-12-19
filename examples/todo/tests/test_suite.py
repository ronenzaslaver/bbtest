""" How to test a todo?

This Module includes the test suite that verifies the todo component using
a black box methodology.

"""
from bbtest import BBTestCase, LocalHost
from . import ToDoBox


class ToDoTest(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [ToDoBox],
         },
    }

    def test_add(self):
        box = self.lab.boxes[ToDoBox.NAME][0]
        box.add("Foo")
        todos = box.list()
        self.assertEqual(todos, ["Foo"])


class DoubleToDoTest(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [ToDoBox, ToDoBox],
         },
    }

    def test_add(self):
        todo_box1 = self.lab.boxes[ToDoBox.NAME][0]
        todo_box2 = self.lab.boxes[ToDoBox.NAME][1]
        todo_box1.add("Foo")
        todos = todo_box1.list()
        self.assertEqual(todos, ["Foo"])
        self.assertFalse(todo_box2.list())
