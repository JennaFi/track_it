from datetime import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habits.models import Habit
from habits.tasks import send_habit_reminder
from users.models import User


class HabitTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test1@test1.com')
        self.habit = Habit.objects.create(name='Jogging',
                                          time=time(12, 0), action='Useful habit', user=self.user
                                          )

        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        url = reverse('habits:habit_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.habit.pk,
                    "name": "Jogging",
                    "action_time": 0,
                    "frequency": 1,
                    "location": "Anywhere",
                    "time": "12:00:00",
                    "action": "Useful habit",
                    "is_pleasant_habit": False,
                    "award": None,
                    "is_public": False,
                    "user": self.user.pk,
                    "connected_habit": None,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_habit_retrieve(self):
        url = reverse('habits:habit_detail', args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('action'), self.habit.action)

    def test_habit_create(self):
        url = reverse('habits:habit_create')

        data = {
            "name": "Jogging",
            "action_time": 0,
            "frequency": 1,
            "location": "Anywhere",
            "time": "12:01:00",
            "action": "Useful habit",
            "is_pleasant_habit": True,
            "user": self.user.pk,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_update(self):
        url = reverse('habits:habit_create')

        data = {
            "time": "12:01:00",
            "action": "Useful habit",
            "is_pleasant_habit": True,
            "user": self.user.pk,
        }

        self.client.post(url, data)

        url = reverse('habits:habit_update', args=(self.habit.pk,))
        data = {'connected_habit': Habit.objects.get(action='Useful habit').pk}
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get('connected_habit'), Habit.objects.get(action='Useful habit').pk
        )

    def test_habit_delete(self):
        url = reverse('habits:habit_delete', args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
