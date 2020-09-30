from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, UserViewSet, HistoryViewSet

app_name = "tasks"

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
router.register(r'history', HistoryViewSet, basename='history')
router.register(r'users', UserViewSet, basename='users')
urlpatterns = router.urls
