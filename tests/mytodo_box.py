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

    def run(self, args_in, **kwargs):

        mytodo_py = self.host.join(self.path, 'mytodo.py')
        args = [mytodo_py ] + list(args_in)
        logger.info(f'{self.__class__.__name__} command: host.run({args} {kwargs})')
        result = self.host.run_python3(args, **kwargs)
        logger.info(f"{self.__class__.__name__} returns: {result}")
        return result

    def add(self, todo):
        return self.run(['add', todo])

    def delete(self, todo):
        return self.run(['del', todo])

    def list(self):
        return self.run(['list'])

    def do_nothing(self):
        return self.run(['nothing'])

    def uninstall(self):
        return self.host.rmtree(self.path)

    def clean(self):
        return self.host.rmfile(self.host.join(self.path, 'todo.txt'))
