""" Code to answer: How to test an installer?

This Module includes the test suite that verifies the installer using the
black box methodology.

"""
import os

import bbtest


class InstallerTest(bbtest.BBTestCase):
    """This test case test a simple installer.

    Our sample installer gets one parameter - the server address - and
    installs a scripts that posts the message "Hello Sara" to the server.
    """
    LAB = {
        'client': {
            'class': bbtest.LocalHost,
            'boxes': [bbtest.HomeBox],
         },
        'server': {
            'class': bbtest.LocalHost,
            'boxes': [bbtest.ServerSpyBox],
         },
    }

    def test_install(self):
        src_dir = os.path.dirname(os.path.dirname(__file__))
        home_box = self.lab.boxes[bbtest.HomeBox.NAME][0]
        host = home_box.host
        installer_path = host.join(home_box.path, 'installer.bash')

        server_box = self.lab.boxes[bbtest.ServerSpyBox.NAME][0]
        registration_url = server_box.url

        # Next lines were copied from the ToDoBox sample code
        host.put(os.path.join(src_dir, 'installer.sh'), installer_path)

        home_box.run('chmod', '777', installer_path)
        home_box.run(installer_path, registration_url)
        exec_path = host.join(home_box.path, 'bbtest.installer.example.sh')
        self.assertTrue(host.isfile(exec_path))
        home_box.run(exec_path)
        self.assertEqual(server_box.log,
                         ["Hello Sara!"])
