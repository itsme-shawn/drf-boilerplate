""" 
Tests for the user API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .utils import *

CREATE_USER_URL = reverse("user:create")
ME_URL = reverse("user:me")


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

    def test_retrieve_user_unauthorized(self):
        """인증되지 않은 유저가 프로필을 조회하면 401 코드 리턴"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """인증이 필요한 로직 테스트"""

    def setUp(self):
        self.user = create_user(
            email="test@example.com",
            password="testpass123",
            name="Test Name",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """로그인 유저의 프로필 조회 테스트"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name, "email": self.user.email})

    def test_post_me_not_allowed(self):
        """프로필 api에 POST 요청이 막혀있는지 확인하는 테스트"""
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """인증된 유저에 대해 프로필 업데이트 테스트"""
        payload = {"name": "updated name", "password": "newpassword"}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
