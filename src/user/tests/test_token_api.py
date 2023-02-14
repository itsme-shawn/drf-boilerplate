""" 
Tests for the token API
"""


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .utils import *

TOKEN_URL = reverse("user:token")


class PublicTokenApiTests(TestCase):
    """public 로 열린 token API 테스트"""

    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """valid한 유저의 토큰 생성 테스트"""
        user_details = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "test-user-password123",
        }

        create_user(**user_details)

        payload = {"email": user_details["email"], "password": user_details["password"]}

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """잘못된 유저 비밀번호에 대해서 토큰 미발급"""
        create_user(email="test@example.com", password="goodpass")

        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """잘못된 유저 이메일에 대해서 토큰 미발급"""
        payload = {"email": "test@example.com", "password": "invalidpass"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """빈 패스워드에 대해서 토큰 미발급"""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
