import pytest
from rest_framework import viewsets
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from account.models import User

@pytest.fixture
def common_user():
    return User.objects.create_user(email="test@test.com", password="test12345")

@pytest.mark.django_db
class TestPostApi:
    client = APIClient()

    def test_get_post_response_200_status(self):
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_post_response_401_status(self):
        url = reverse("blog:api-v1:post-list")
        data={
            "title": "test",
            "content": "test",
            "status": True,
            "pub_date": datetime.now(),
        }
        response = self.client.post(url,data)
        assert response.status_code == 401

    def test_create_post_response_201_status(self,common_user):
        url = reverse("blog:api-v1:post-list")
        data={
            "title": "test",
            "content": "test",
            "status": True,
            "pub_date": datetime.now(),
        }
        self.client.force_login(user=common_user)
        response = self.client.post(url,data)
        assert response.status_code == 201

    def test_create_post_response_400_status(self,common_user):
        url = reverse("blog:api-v1:post-list")
        data={
            "title": "test",
            "content": "test"
        }
        self.client.force_login(user=common_user)
        response = self.client.post(url,data)
        assert response.status_code == 400
