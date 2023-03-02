import pytest
from rest_framework import status
from api.models import *


@pytest.mark.django_db
class TestAssignmentView:
    def test_if_user_is_none(self,api_client):
        endpoint = "/api/assignments/"
        response = api_client.get(endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_none(self,api_client,authenticate):
        authenticate()
        endpoint = "/api/assignments/"
        response = api_client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_staff(self,api_client,authenticate):
        authenticate(is_staff=True)
        endpoint = "/api/assignments/"
        response = api_client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK

