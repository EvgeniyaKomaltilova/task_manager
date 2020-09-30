from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet

app_name = "tasks"

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
urlpatterns = router.urls
