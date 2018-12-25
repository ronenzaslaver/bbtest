
from bbtest import BBTestCase, LocalHost
from .mytodo_box import MyToDoBox


class ToDoTest(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [MyToDoBox],
         },
    }

    def test_operations(self):
        box = self.lab.boxes[MyToDoBox.NAME][0]
        box.add("Foo")
        todos = box.list()
        self.assertEqual(todos, ['Foo'])


class DoubleToDoTest(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [MyToDoBox, MyToDoBox],
         },
    }

    def test_add(self):
        todo_box1 = self.lab.boxes[MyToDoBox.NAME][0]
        todo_box2 = self.lab.boxes[MyToDoBox.NAME][1]
        todo_box1.add('Foo')
        todos = todo_box1.list()
        self.assertEqual(todos, ['Foo'])
        self.assertFalse(todo_box2.list())
