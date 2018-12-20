import logging
import os

from bbtest import BlackBox

logger = logging.getLogger('bblog')


class ToDoBox(BlackBox):
    """A black box wrapper for todo.sh.
    Like every black box, the todo box has the `install` and `clean`
    (TODO: uninstall?) methods. On top of that we have methods to be used
    by the test coders to poke the box and peek into it.
    """

    NAME = 'todo'

    def install(self):
        """ installing todo.txt
        First creates a temp dir on the host and then coppies the assets
        in. On Linux, we need to make sure `todo.sh` is executable.
        """
        self.home = self.mkdtemp()
        src_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'src')
        dest_dir = self.home

        for asset in ['todo.sh', 'todo.cfg']:
            self.host.put(os.path.join(src_dir, asset),
                          remote=self.host.join(dest_dir, asset))

        if self.host.os == 'linux':
            self.host.run('chmod', '777', self.host.join(self.home, "todo.sh"))

    def run(self, *args):
        """Pass the args to a todo.sh running on the host. See `todo.sh -h`
        for more details.
        """
        todo_sh = self.host.join(self.home, 'todo.sh')
        logger.info(f"ToDoBox Starts: {todo_sh} {args}")
        result = self.host.run(todo_sh, *args)
        logger.info(f"ToDoBox returns: {result}")
        return result

    def add(self, todo):
        """Add a to do.
        Add is a *Porceline method* - one that adds only a shining interface.
        The same function can be achived by using the low level, aka `plumbing`
        methods.
        """
        return self.run('add', todo)

    def list(self):
        """Return a list of todos."""
        todos = list()
        list_out = self.run('list')
        for line in list_out[:-2]:
            todos.append(line[2:])
        return todos

    def remove(self):
        """Remove our home directory"""
        return self.host.rmtree(self.home)

    def clean(self):
        """Clean's job is to wipe all data. In todo's case, it's just a file"""
        return self.host.rmfile(self.host.join(self.home, 'todo.txt'))

