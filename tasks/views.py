from django.contrib.auth.models import User
from django.http.response import HttpResponse
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from tasks.models import Task
from tasks.serializers import TaskSerializer, UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """View for task api"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    """View for task api"""
    permission_classes = (AllowAny,)
    http_method_names = ['post', 'head']
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class CreateUserAPIView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#         user = request.data
#         serializer = UserSerializer(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
