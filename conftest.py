
import pytest


def pytest_addoption(parser):
    parser.addoption('--os', action='store', default='local', help='OS type of traget machine - local, windows or linux')
    parser.addoption('--ip', action='store', default='localhost', help='IP address of target machine')
    parser.addoption('--user', action='store', default='Administrator', help='Username for target machine')
    parser.addoption('--pw', action='store', default='Password1', help='Password for target machine')
