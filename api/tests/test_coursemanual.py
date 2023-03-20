import json

import pytest
from model_bakery import baker
from rest_framework import status

from api.models import *
from api.utils import convert_to_dot_notation


@pytest.mark.django_db
class TestCourseManualViewSet:

    endpoint = "/api/coursemanuals/"

    def test_if_user_is_none(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_none(self, api_client, authenticate):
        authenticate()
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_staff(self, api_client, authenticate):
        authenticate(is_staff=True)    
        response = api_client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK

        