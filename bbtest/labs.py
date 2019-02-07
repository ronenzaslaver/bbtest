
from .exceptions import ImproperlyConfigured


class Lab():

    def __init__(self, topology={}, address_book={}):
        """
        :param topology: a dictionary representing the topology of the test setup.
                         each hostname in the dictionary is a dictionary with `class` & `boxes`
        :param address_book: a dictionary where each hostname has
                             a dictionary with ip, username & password
        """
        self.boxes = {}
        self.hosts = {}
        self.pip_index = topology.get('pip_index', 'https://pypi.org/simple')
        self.auth = topology.get('auth', None)

        if 'hosts' not in topology:
            return

        for host_name, params in topology['hosts'].items():
            if 'class' not in params:
                raise ImproperlyConfigured(f"Host '{host_name}' must have a `class` key")
            if 'boxes' not in params:
                raise ImproperlyConfigured(f"Host '{host_name}' must have a `boxes` key")
            host_class = params['class']
            try:
                host = host_class(name=host_name, pip_index=self.pip_index, **address_book[host_name])
            except KeyError:
                # TODO: allocate a host, use params['image']
                host = host_class(name=host_name, pip_index=self.pip_index)
            self.hosts[host_name] = host
            self.hosts[host_name].install(package=params.get('package', None))
            # let there be boxes!
            for box_class in params['boxes']:
                self.add_box(box_class, host)

    def add_box(self, box_class, host):
        new_box = box_class(host)
        new_box.install()
        box_name = new_box.NAME
        if box_name in self.boxes:
            self.boxes[box_name].append(new_box)
        else:
            self.boxes[box_name] = [new_box]
        return new_box

    def flatten_boxes(self):
        """ an iterator returning  one box after the other """
        for boxes in self.boxes.values():
            for box in boxes:
                yield box

    def destroy(self):
        """Destroy lab altogether """
        for box in self.flatten_boxes():
            box.uninstall()
        for host in self.hosts.values():
            host.uninstall()
        self.boxes = {}
        self.hosts = {}

    def clean(self):
        """Restore the lab back to its original condition """
        for box in self.flatten_boxes():
            box.clean()
        for host in self.hosts.values():
            host.clean()
