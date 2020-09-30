from django.contrib.auth.models import User
from rest_framework import serializers
from tasks.models import Task, History


class TaskSerializer(serializers.ModelSerializer):
    """Task model serializer"""

    class Meta:
        model = Task
        fields = (
            'title',
            'description',
            'date_of_creation',
            'status',
            'planned_completion_date',
            'user',
            # 'history',
        )
    # history = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class HistorySerializer(serializers.ModelSerializer):
    """History model serializer"""

    class Meta:
        model = History
        fields = (
            'task',
            'title',
            'description',
            'date_of_creation',
            'date_of_change',
            'status',
            'planned_completion_date',
            'user',
        )


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )
