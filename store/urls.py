from rest_framework.routers import DefaultRouter
from .views import *

product_router = DefaultRouter()
product_router.register(r'', ProductViewSet, basename='product')

collection_router = DefaultRouter()
collection_router.register(r'', CollectionViewSet, basename='collection')

order_router = DefaultRouter()
order_router.register(r'', OrderViewSet, basename='order')
