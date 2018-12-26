
from .exceptions import ImproperlyConfigured


class Lab():

    def __init__(self, lab, address_book={}):
        """
        :param lab: a dictionary where each hostname has
                    a dictionary with `image` & `boxes`
        :param address_book: a dictionary where each hostname has
                             a dictionary with ip, username & password
        """
        self.boxes = {}
        self.hosts = {}
        for host_name, params in lab.items():
            if 'class' not in params:
                raise ImproperlyConfigured(f"Host '{host_name}' must have a `class` key")
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
            host.destroy()
        self.boxes = {}
        self.hosts = {}

    def clean(self):
        """Restore the lab back to its original condition """
        for box in self.flatten_boxes():
            box.clean()
        for host in self.hosts.values():
            host.clean()
