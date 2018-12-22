
from bbtest import BBTestCase, LocalHost
from .pytodo_box import PyToDoBox


class ToDoTest(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [PyToDoBox],
         },
    }

    def test_operations(self):
        box = self.lab.boxes[PyToDoBox.NAME][0]
        box.add("Foo")
        todos = box.list()
        self.assertEqual(todos, ['Foo'])


class DoubleToDoTest(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [PyToDoBox, PyToDoBox],
         },
    }

    def test_add(self):
        todo_box1 = self.lab.boxes[PyToDoBox.NAME][0]
        todo_box2 = self.lab.boxes[PyToDoBox.NAME][1]
        todo_box1.add('Foo')
        todos = todo_box1.list()
        self.assertEqual(todos, ['Foo'])
        self.assertFalse(todo_box2.list())
