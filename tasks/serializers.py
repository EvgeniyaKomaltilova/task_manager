from rest_framework import serializers
from tasks.models import Task


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
            'history',
        )

    history = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

