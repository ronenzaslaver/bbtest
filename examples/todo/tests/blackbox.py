import logging

from bbtest import BlackBox, BBTestCase

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
        self.host.put("examples/todo/src/todo.sh", remote="/tmp/todo.sh")
        self.host.put("examples/todo/src/todo.cfg", remote="/tmp/todo.cfg")

    def clean(self, msg):
        return self.host.run('rm todo.txt')

    def run(self, msg):
        """Pass on a todo.sh command  such ass add, list, etc """
        logger.info(f"ToDoBox Starts: {msg}")
        result = self.host.run(f'/tmp/todo.sh {msg}')
        logger.info(f"ToDoBox returns: {result}")
        return result

    def add(self, todo):
        return self.run(f'add {todo}')

    def list (self):
        todos = []
        list_out = self.run('list')
        for line in list_out[:-2]:
            todos.append(line[2:])
        return todos
