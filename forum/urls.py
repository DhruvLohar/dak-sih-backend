from rest_framework.routers import DefaultRouter
from .views import ForumPostViewSet

router = DefaultRouter()
router.register(r'', ForumPostViewSet, basename='forum')
