import logging
import os

from bbtest import BlackBox

logger = logging.getLogger('bblog')


class MyToDoBox(BlackBox):

    NAME = 'mytodo'

    def install(self):
        self.home = self.mkdtemp()
        src_dir = os.path.join(os.path.dirname(__file__), 'src')
        dest_dir = self.home

        self.host.put(os.path.join(src_dir, 'mytodo.py'),
                      remote=self.host.join(dest_dir, 'mytodo.py'))

        if self.host.os == 'linux':
            self.host.run('chmod', '777', self.host.join(self.home, 'mytodo.py'))

    def run(self, *args):
        todo_py = self.host.join(self.home, 'mytodo.py')
        logger.info(f"PyToDoBox command: {todo_py} {args}")
        result = self.host.run(todo_py, *args)
        logger.info(f"PyToDoBox returns: {result}")
        return result

    def add(self, todo):
        return self.run('add', todo)

    def delete(self, todo):
        return self.run('del', todo)

    def list(self):
        return self.run('list')

    def remove(self):
        return self.host.rmtree(self.home)

    def clean(self):
        return self.host.rmfile(self.host.join(self.home, 'todo.txt'))
