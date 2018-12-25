import logging
import os

from bbtest import HomeBox

logger = logging.getLogger('bblog')


class MyToDoBox(HomeBox):

    NAME = 'mytodo'

    def install(self):
        super().install()
        src_dir = os.path.join(os.path.dirname(__file__), 'src')

        self.host.put(os.path.join(src_dir, 'mytodo.py'),
                      remote=self.host.join(self.path, 'mytodo.py'))

        if self.host.os == 'linux':
            self.host.run('chmod', '777', self.host.join(self.path, 'mytodo.py'))

    def run(self, *args):
        todo_py = self.host.join(self.path, 'mytodo.py')
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
        return self.host.rmtree(self.path)

    def clean(self):
        return self.host.rmfile(self.host.join(self.path, 'todo.txt'))
