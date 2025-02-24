from django.db import models

from config.settings import AUTH_USER_MODEL


class Habit(models.Model):
    """Habit model"""
    name = models.CharField(max_length=100, verbose_name='Habit')
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User', blank=True, null=True)
    location = models.CharField(max_length=50, default='Anywhere', verbose_name='Location')
    time = models.TimeField(verbose_name='Time', blank=True, null=True)
    frequency = models.PositiveIntegerField(verbose_name='Frequency', default=1, blank=True, null=True)
    action = models.CharField(max_length=50, verbose_name='Action', blank=True, null=True)
    is_pleasant_habit = models.BooleanField(default=False, verbose_name='is_pleasant')
    connected_habit = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Connected habit', blank=True,
                                        null=True)
    award = models.CharField(max_length=50, null=True, blank=True, verbose_name='Award')
    action_time = models.PositiveIntegerField(default=0, verbose_name='Time to act in seconds')
    is_public = models.BooleanField(default=False, verbose_name='is_public')

    class Meta:
        verbose_name = 'Habit'
        verbose_name_plural = 'Habits'
        ordering = ['pk', ]

    def __str__(self):
        return f"{self.user} - {self.action}"
