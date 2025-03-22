from rest_framework import serializers


def validate_action_time(value):
    """Validates the time of action"""
    if value not in range(121):
        raise serializers.ValidationError('Time of action must be up to 120 seconds')


def validate_frequency(value):
    """Validates the frequency of habit"""
    if value not in range(1, 8):
        raise serializers.ValidationError('The frequency can be up from 1 to 7 days')


def validate_connected_habit(attrs, field_name='connected_habit'):
    """Validates if habit is pleasant as connected can be only pleasant habit"""

    connected_habit = attrs.get(field_name)
    if connected_habit and not connected_habit.is_pleasant_habit:
        raise serializers.ValidationError(
            {field_name: 'Connected habit should be marked as a pleasant one.'}
        )


def validate_pleasant_habit(attrs):
    """Validates if habit has a prize or connected habit"""

    is_pleasant_habit = attrs.get('is_pleasant_habit')
    connected_habit = attrs.get('connected_habit')
    award = attrs.get('award')
    if is_pleasant_habit and (connected_habit or award):
        raise serializers.ValidationError(
            {'Pleasant habit can not has an award or connected habit.'})


def validate_award_and_connected_habit(attrs, fields):
    """Validates if only one field is filled or no one"""

    filled_fields = [field for field in fields if attrs.get(field) not in (None, '')]

    if len(filled_fields) > 1:
        raise serializers.ValidationError(
            f"You can fill only one field: {', '.join(fields)}."
        )
