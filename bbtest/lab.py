
class Lab():

    boxes = {}
    hosts = {}

    def __init__(self, lab):
        for host_name, host in lab.items():
            self.hosts[host_name] = self.get_host(host)

            for box_class in host['boxes']:
                box = box_class()
                self.boxes[host_name] = box

    def clean(self):
        """Restore the lab back to its original condition """
        for box in self.boxes:
            box.clean()
        for host in self.hosts:
            host.clean()
