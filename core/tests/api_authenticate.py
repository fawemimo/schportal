import pytest

from api.models import *


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_active=True,is_staff=False):
        return api_client.force_authenticate(user=User(is_active=is_active,is_staff=is_staff))
    return do_authenticate    