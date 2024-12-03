from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'products', ExchangeProductViewSet, basename='exchange-products')
router.register(r'orders', ExchangeOrderViewSet, basename='exchange-orders')

