"""
Default conftest for bbtest tests cases.
Copy this file to each and every folder that contains bbtest test cases.
"""

import pytest


@pytest.fixture(scope='class', autouse=True)
def create_destroy_lab(request):
    request.cls.create_lab()
    yield
    request.cls.destroy_lab()


@pytest.fixture(autouse=True)
def setup_clean_lab(request):
    request.instance.setup_lab()
    yield
    request.instance.clean_lab()
