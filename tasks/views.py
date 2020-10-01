import jwt
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.serializers import jwt_payload_handler
from task_manager import settings
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
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    search_fields = ['status', 'planned_completion_date']
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class HistoryViewSet(viewsets.ModelViewSet):
    """View for history api"""
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'head']
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    filter_backends = [HistoryFilter]


class UserViewSet(viewsets.ModelViewSet):
    """View for user api"""
    permission_classes = (AllowAny,)
    http_method_names = ['post', 'head']
    queryset = User.objects.all()
    serializer_class = UserSerializer


# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# def authenticate_user(request):
#     try:
#         username = request.data['username']
#         password = request.data['password']
#
#         user = User.objects.get(username=username, password=password)
#         if user:
#             try:
#                 payload = jwt_payload_handler(user)
#                 token = jwt.encode(payload, settings.SECRET_KEY)
#                 user_details = {}
#                 user_details['id'] = user.id
#                 user_details['token'] = token
#                 user_logged_in.send(sender=user.__class__, request=request, user=user)
#                 return HttpResponse(user_details, status=status.HTTP_200_OK)
#
#             except Exception as e:
#                 raise e
#         else:
#             res = {
#                 'error': 'can not authenticate with the given credentials or the account has been deactivated'}
#             return HttpResponse(res, status=status.HTTP_403_FORBIDDEN)
#     except KeyError:
#         res = {'error': 'please provide a email and a password'}
#         return HttpResponse(res)
#
