""" 
Tests for the user API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")

# 유틸함수
def create_user(**params):
    """create된 유저를 return함"""
    return get_user_model().objects.create_user(**params)  # type: ignore


class PublicUserApiTests(TestCase):
    """public 로 열린 user API 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """user create 성공 테스트"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test name",
        }
        res = self.client.post(path=CREATE_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_with_email_exists_error(self):
        """기존 메일로 가입하려고 할 시 에러발생"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test name",
        }
        create_user(**payload)

        res = self.client.post(path=CREATE_USER_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """비밀번호 길이 너무 짧을 시 에러발생"""
        payload = {
            "email": "test@example.com",
            "password": "123",
            "name": "Test name",
        }
        res = self.client.post(path=CREATE_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # DB에 저장 안 됐는지 확인
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)
