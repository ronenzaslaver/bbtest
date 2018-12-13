""" How to test a todo?

This Module includes the test suite that verifies the todo component using
a black box methodology.

"""
from bbtest import BBTestCase
from . import ToDoBox


class ToDoTest(BBTestCase):

    LAB = {
        'host1': {
            'image': "linux",
            'boxes': [ ToDoBox, ],
         },
    }

    def test_add(self):
        todo_box = self.boxes[ToDoBox.name]
        todo_box.add("Foo")
        todos = todo_box.list()
        assert todos == ["Foo"]
