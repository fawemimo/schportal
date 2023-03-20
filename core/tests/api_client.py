import pytest
from rest_framework.test import APIClient

from api.models import *


@pytest.fixture
def api_client():
    return APIClient()