""" Code to answer: How to test an installer?

This Module includes the test suite that verifies the installer using the
black box methodology.

"""
import os

import bbtest


class InstallerTest(bbtest.BBTestCase):

    LAB = {
        'client': {
            'class': bbtest.OSXHost,
            'boxes': [bbtest.HomeBox],
         },
        'server': {
            'class': bbtest.LinuxHost,
            'boxes': [bbtest.ServerSpyBox],
         },
    }

    def test_install(self):
        src_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'src')
        home_box = self.lab.boxes[bbtest.HomeBox.NAME][0]
        host = home_box.host
        installer_path = host.join(home_box.path, 'installer.sh')

        server_box = self.lab.boxes[bbtest.ServerSpyBox.NAME][0]
        registration_url = server_box.url

        # Next lines were copied from the ToDoBox sample code
        home_box.put(os.path.join(src_dir, 'installer.sh'), installer_path)

        host.run('chmod', '777', installer_path)
        host.run(installer_path, {'server_url': registration_url})
        self.assertTrue(host.path.isfile('/tmp/bbtest.installer.example.sh'))
        host.run('/tmp/bbtest.installer.example.sh')
        self.assertEqual(server_box.log,
                         ["Hello Sara"])
