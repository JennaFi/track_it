from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.pagination import CustomPagination
from users.models import User
from users.permissions import IsUser, IsOwner
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """User viewset"""

    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.is_active = True
        user.save()
        return user

    def perform_update(self, serializer):
        user = serializer.instance
        user.set_password(serializer.validated_data['password'])
        user.save()

        return super().perform_update(serializer)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsAuthenticated, IsUser]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
