
from copy import deepcopy

from .exceptions import ImproperlyConfigured
from .blackboxes import BlackBox


class Lab():

    def __init__(self, topology={}, address_book={}):
        """
        :param topology: a dictionary representing the topology of the test setup.
                         each hostname in the dictionary is a dictionary with `class` & `boxes`
        :param address_book: a dictionary where each hostname has
                             a dictionary with ip, username & password
        """

        self.topology = deepcopy(topology)

        self.hosts = {}
        self.pip_index = self.topology.get('pip_index', 'https://pypi.org/simple')
        self.auth = self.topology.get('auth', None)

        if 'hosts' not in self.topology:
            return

        # let there be hosts!
        for host_name, host_params in self.topology['hosts'].items():
            if 'class' not in host_params:
                raise ImproperlyConfigured(f"Host '{host_name}' must have a `class` key")
            host_address = address_book.get(host_name, {})
            self.add_host(host_params.pop('class'), host_name, host_params, host_address)

    def add_host(self, host_class, name, params={}, address_book={}):
        """Adding a new host to the lab"""
        boxes = params.pop('boxes', {})
        try:
            host = host_class(name=name, pip_index=self.pip_index, **{**params, **address_book})
        except KeyError:
            # TODO: allocate a host, use params
            host = host_class(name=name, pip_index=self.pip_index, **params)
        self.hosts[name] = host
        self.hosts[name].install(package=params.get('package', None))

        host.boxes = {}
        if not boxes:
            return

        # let there be boxes!
        for box_name, box_params in boxes.items():
            if 'class' not in box_params:
                raise ImproperlyConfigured(f"Box '{box_name}' must have a `class` key")
            self.add_box(box_params['class'], host, box_name, box_params)

        return self.hosts[name]

    def add_box(self, box_class, host, name, params={}):
        """Adding a new box to the lab"""
        box = box_class(name, host, **params)
        box.install()
        host.boxes[name] = box
        return host.boxes[name]

    @property
    def boxes(self):
        boxes = {}
        for host in self.hosts.values():
            for box in host.boxes.values():
                boxes[f'{host}.{box}'] = box
        return boxes

    def class_boxes(self, box_class=BlackBox):
        return {n: c for n, c in self.boxes.items() if isinstance(c, box_class)}

    def destroy(self):
        """Destroy lab altogether """
        for host in self.hosts.values():
            for box in host.boxes.values():
                box.uninstall()
            host.boxes = {}
            host.uninstall()
        self.hosts = {}

    def clean(self):
        """Restore the lab back to its original condition """
        for host in self.hosts.values():
            for box in host.boxes.values():
                box.clean()
            host.clean()
