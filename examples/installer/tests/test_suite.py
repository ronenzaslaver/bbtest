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
            'boxes': [bbtest.SpyServerBox],
         },
    }

    FILENAME = 'installer.sh'

    def test_install(self):
        server_box  = self.lab.boxes[bbtest.SpyServerBox.NAME][0]
        home_box    = self.lab.boxes[bbtest.HomeBox.NAME][0]
        host        = home_box.host
        src_path    = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                    self.FILENAME)
        home_box.run_file(src_path, params=[server_box.url])

        exec_path = host.join(home_box.path, 'bbtest.installer.example.sh')
        self.assertTrue(host.isfile(exec_path))

        home_box.run(exec_path)
        self.assertEqual(server_box.log, ["Hello Sara!"])
