"""
Default conftest for bbtest tests cases.
Copy this file to each and every folder that contains bbtest test cases.
"""

import pytest


def pytest_addoption(parser):
    parser.addoption('--pip-index', action='store', default='',
                     help='url of python package index to use or full path to local directory')


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
