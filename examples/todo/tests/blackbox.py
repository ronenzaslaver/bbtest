import yaml
from bbtest import BlackBox, BBTestCase


class ToDoBox(BlackBox):
    """A thin wrapper for todo.sh, just pass the message on
       https://github.com/todotxt/todo.txt-cli

       the first thing the box does is name itself by concatenating the
       `NAME_PREFIX` and an optional suffix provides the case writer. The
       test writer can't overide the prefix so we keep a clean dictionary
       with less ambiguaty regarding lab's assets.
    """
    NAME_PREFIX = "todo"

    def install(self):
        pass

    def clean(self, msg):
        return self.host.run('rm todo.txt')

    def cmd(self, msg):
        """Pass on a todo.sh command  such ass add, list, etc """
        return self.host.run(f'todo.sh {msg}')

    def add(self, todo):
        return self.host.run(f'add {todo}')

    def list (self, todo):
        todos = []
        list_out = self.host.run('list')
        for i in list_out[:-2]:
            todos.append(line[2:])
        return todos

