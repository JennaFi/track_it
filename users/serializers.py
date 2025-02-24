from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = User
        fields = ('id', 'email', 'tg_chat_id', 'password',)
