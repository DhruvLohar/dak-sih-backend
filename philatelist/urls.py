from rest_framework.routers import DefaultRouter
from .views import PhilatelistAPIView

router = DefaultRouter()
router.register(r'', PhilatelistAPIView, basename='philatelist')
