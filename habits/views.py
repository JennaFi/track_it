from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import CustomPagination
from habits.serializers import HabitSerializer
from habits.services import send_telegram_message
from users.permissions import IsOwner


class HabitListAPIView(generics.ListAPIView):
    """List of habits"""
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, IsOwner]


class HabitPublicListAPIView(generics.ListAPIView):
    """List of HabitPublic"""

    serializer_class = HabitSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Habit in detail"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_response(self, request, response, *args, **kwargs):
        response = super().get_response(request, response, *args, **kwargs)
        print(response.data.get('action'))
        print(request.user.tg_chat_id)
        send_telegram_message(request.user.tg_chat_id, response.data.get('action'))
        return response


class HabitCreateAPIView(generics.CreateAPIView):
    """Creation of Habit"""

    serializer_class = HabitSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Update Habit"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Delete Habit"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
