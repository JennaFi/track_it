from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitRetrieveAPIView, HabitUpdateAPIView, HabitDestroyAPIView, \
    HabitCreateAPIView, HabitPublicListAPIView, HabitListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habit_list'),
    path('habits/public', HabitPublicListAPIView.as_view(), name='habit_public_list'),
    path('habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_detail'),
    path('habits/<int:pk>/update', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habits/<int:pk>/delete', HabitDestroyAPIView.as_view(), name='habit_delete'),
    path('habits/create', HabitCreateAPIView.as_view(), name='habit_create'),

]
