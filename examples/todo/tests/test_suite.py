""" How to test a todo?

This Module includes the test suite that verifies the todo component using
a black box methodology.

"""
from bbtest import BBTestCase, LocalHost
from . import ToDoBox


class BaseToDoTest(BBTestCase):

    def setUp(self):
        """ clean the todo.txt before each test method """
        super().setUp()
        self.todo_box = self.lab.boxes[ToDoBox.NAME][0]
        self.todo_box.clean()


class ToDoTest(BaseToDoTest):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [ToDoBox],
         },
    }

    def test_add(self):
        self.todo_box.add("Foo")
        todos = self.todo_box.list()
        assert todos == ['Foo']


class DoubleToDoTest(BaseToDoTest):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [ToDoBox, ToDoBox],
         },
    }

    def test_add(self):
        self.todo_box.add("Foo")
        todos = self.todo_box.list()
        assert todos == ['Foo']
        todo_box2 = self.lab.boxes[ToDoBox.NAME][1]
        assert not todo_box2.list()
