"""
Default conftest for bbtest tests cases.
Copy this file to each and every folder that contains bbtest test cases.
"""

import pytest


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
