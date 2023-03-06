import pytest 
from api.models import *
from rest_framework import status
from model_bakery import baker


@pytest.mark.django_db
class TestProjectViewSet:

    def test_if_user_is_none(self,api_client):
        endpoint = "/api/projects/"
        response = api_client.get(endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_none(self, api_client, authenticate):
        authenticate()
        endpoint = "/api/projects/"
        response = api_client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK    

    def test_if_user_is_staff(self, api_client, authenticate):    
        authenticate(is_staff=True,is_active=False)
        endpoint = "/api/projects/"
        response = api_client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK

    def test_get_project_by_id(self, api_client, authenticate):    
        authenticate()
        project = baker.make(ProjectAllocation)
        print(project.__dict__)
        response = api_client.get(f"/api/projects/{project.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "student": project.student,
            "project": project.project,
            "supervisor": project.supervisor,
            "start_date": project.start_date,
            "delivery_status": project.delivery_status,
        }