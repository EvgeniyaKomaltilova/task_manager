from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from tasks.models import Task, History
from tasks.serializers import TaskSerializer, UserSerializer, HistorySerializer


class HistoryFilter(filters.BaseFilterBackend):
    """Custom filter by task for history model"""

    def filter_queryset(self, request, queryset, view):
        """filter history by task id"""
        return queryset.filter(task=request.GET['task']).order_by('-date_of_change')


class TaskFilter(filters.BaseFilterBackend):
    """Custom filter by status and planned completion date for task model"""

    def filter_queryset(self, request, queryset, view):
        """filter task queryset by status and planned completion date"""

        if request.GET.get('status', '') and request.GET.get('planned_completion_date', ''):
            return queryset.filter(
                status=request.GET.get('status', ''),
                planned_completion_date=request.GET.get('planned_completion_date', '')
            )

        elif request.GET.get('status', ''):
            return queryset.filter(status=request.GET.get('status', ''))

        elif request.GET.get('planned_completion_date', ''):
            return queryset.filter(planned_completion_date=request.GET.get('planned_completion_date', ''))

        return queryset


class TaskViewSet(viewsets.ModelViewSet):
    """View for task api"""
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    filter_backends = [TaskFilter]

    def get_queryset(self):
        """user can get only his own tasks"""
        return Task.objects.filter(user=self.request.user)


class HistoryViewSet(viewsets.ModelViewSet):
    """View for history api"""
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'head']
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    filter_backends = [HistoryFilter]

    def get_queryset(self):
        """user can get history about only his own tasks"""
        return History.objects.filter(user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """View for user api"""
    permission_classes = (AllowAny,)
    http_method_names = ['post', 'head']
    queryset = User.objects.all()
    serializer_class = UserSerializer
