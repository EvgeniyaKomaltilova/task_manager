from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, UserViewSet

app_name = "tasks"

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'users', UserViewSet, basename='tasks')
urlpatterns = router.urls
