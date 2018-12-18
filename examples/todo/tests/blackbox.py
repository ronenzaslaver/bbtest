import logging
import os

from bbtest import BlackBox

logger = logging.getLogger('bblog')


class ToDoBox(BlackBox):
    """A thin wrapper for todo.sh, just pass the message on
       https://github.com/todotxt/todo.txt-cli

       the first thing the box does is name itself by concatenating the
       `NAME_PREFIX` and an optional suffix provides the case writer. The
       test writer can't overide the prefix so we keep a clean dictionary
       with less ambiguaty regarding lab's assets.
    """

    NAME = 'todo'

    def install(self):
        src_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src')
        self.host.put(os.path.join(src_dir, 'todo.sh'), remote=os.path.join(self.host.temp_dir, 'todo.sh'))
        self.host.put(os.path.join(src_dir, 'todo.cfg'), remote=os.path.join(self.host.temp_dir, 'todo.cfg'))
        if self.host.os == 'linux':
            self.host.run('chmod', '777', os.path.join(self.host.temp_dir, "todo.sh"))

    def clean(self):
        return self.host.run('rm', os.path.join(self.host.temp_dir, 'todo.txt'))

    def run(self, *args):
        """Pass on a todo.sh command  such ass add, list, etc """
        todo_sh = os.path.join(self.host.temp_dir, 'todo.sh')
        logger.info(f"ToDoBox Starts: {todo_sh} {args}")
        result = self.host.run(todo_sh, *args)
        logger.info(f"ToDoBox returns: {result}")
        return result

    def add(self, todo):
        return self.run('add', todo)

    def list(self):
        todos = []
        list_out = self.run('list')
        for line in list_out[:-2]:
            todos.append(line[2:])
        return todos
