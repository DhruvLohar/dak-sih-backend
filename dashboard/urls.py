from rest_framework import routers
from .views import PostalOfficeViewSet, AdminUserViewSet

router = routers.DefaultRouter()
router.register(r'postal-offices', PostalOfficeViewSet)
router.register(r'admin-users', AdminUserViewSet)

urlpatterns = router.urls

