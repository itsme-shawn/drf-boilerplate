"""
Serializers for the user API View
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """password 받아서 validation 통과하면 유저 create & return"""
        return get_user_model().objects.create_user(**validated_data)
        # create_user 함수를 써야하므로 오버라이딩
