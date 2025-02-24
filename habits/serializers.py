from rest_framework import serializers

from habits.models import Habit
from habits.validators import validate_action_time, validate_frequency, validate_connected_habit, \
    validate_pleasant_habit, validate_award_and_connected_habit


class HabitSerializer(serializers.ModelSerializer):
    """Serializer for habit objects"""
    action_time = serializers.IntegerField(default=0, validators=[validate_action_time])
    frequency = serializers.IntegerField(default=1, validators=[validate_frequency])

    def validate_habit(self, attrs):
        validate_connected_habit(attrs, field_name='connected_habit')
        validate_pleasant_habit(attrs)
        validate_award_and_connected_habit(attrs, fields=['award', 'connected_habit'])
        return attrs

    class Meta:
        model = Habit
        fields = '__all__'
