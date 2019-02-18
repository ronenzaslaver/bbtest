"""
Default conftest for bbtest tests cases.
Copy this file to each and every folder that contains bbtest test cases.
Then feel free to change it based on your use case...
"""

import os
import pytest


def pytest_addoption(parser):
    parser.addoption('--pip-index', action='store', default='',
                     help='url of python package index to use or full path to local directory')
    parser.addoption('--topo', action='store', default=os.environ.get('BBTEST_TOPO_YAML', ''),
                     help='path to bbtest lab topology file')
    parser.addoption('--ep-os', action='store', default='local',
                     help='OS of remote host - local, windows, linux oe mac')
    parser.addoption('--ep-ip', action='store', default='',
                     help='IP address of remote host')


@pytest.fixture(scope='class', autouse=True)
def lab_factory(request):
    request.cls.create_lab()
    yield
    request.cls.destroy_lab()


@pytest.fixture(autouse=True)
def clean_lab_factory(request):
    request.instance.setup_lab()
    yield
    request.instance.clean_lab()
