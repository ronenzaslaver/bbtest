from .exceptions import ImproperlyConfigured
from .hosts import Host, LocalHost, LinuxHost, WindowsHost, MacHost


class Lab():

    boxes = {}
    hosts = {}

    def __init__(self, lab, address_book={}):
        """
        :param lab: a dictionary where each hostname has
                    a dictionary with `image` & `boxes`
        :param address_book: a dictionary where each hostname has
                             a dictionary with ip, username & password
        """
        for host_name, params in lab.items():
            if 'class' not in params:
                raise ImproperlyConfigured("A lab's host must have a `class` key")
            host_class = params['class']
            try:
                host = host_class(**address_book[host_name])
            except KeyError:
                # TODO: allocate a host, use params['image']
                host = host_class()
            self.hosts[host_name] = host
            # let there be boxes!
            for box_class in params['boxes']:
                new_box = box_class(host)
                new_box.install()
                box_name = new_box.NAME
                if box_name in self.boxes:
                    self.boxes[box_name].append(new_box)
                else:
                    self.boxes[box_name] = [new_box]

    def clean(self):
        """Restore the lab back to its original condition """
        for box in self.boxes:
            box.clean()
        for host in self.hosts:
            host.clean()
