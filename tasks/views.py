from abc import ABC

from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from tasks.models import Task, History
from tasks.serializers import TaskSerializer, UserSerializer, HistorySerializer


class HistoryFilter(filters.BaseFilterBackend):
    """Custom filter by task for history model"""
    template = 'rest_framework/filters/search.html'
    lookup_prefixes = {
        '@': 'task',
    }

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(task=request.query_params.get('task', ''))


class TaskViewSet(viewsets.ModelViewSet):
    """View for task api"""
    # permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    search_fields = ['status', 'planned_completion_date']
    filter_backends = [filters.SearchFilter]


class HistoryViewSet(viewsets.ModelViewSet):
    """View for history api"""
    # permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'head']
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    # search_fields = ['task__id']
    filter_backends = [HistoryFilter]


class UserViewSet(viewsets.ModelViewSet):
    """View for user api"""
    permission_classes = (AllowAny,)
    http_method_names = ['post', 'head']
    queryset = User.objects.all()
    serializer_class = UserSerializer



