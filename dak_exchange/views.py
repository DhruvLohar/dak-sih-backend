from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import viewsets

from .models import *
from .serializers import *

from dak_sih.permissions import CookieAuthentication
from dak_sih.responses import *

class ExchangeProductViewSet(
    viewsets.ModelViewSet,
    EnhancedResponseMixin
):
    queryset = ExchangeProduct.objects.all()
    serializer_class = ExchangeProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieAuthentication]
    
    @action(detail=False, methods=['get'])
    def my_products(self, request, pk=None):
        products = self.queryset.filter(current_owner=request.user)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExchangeOrderViewSet(
    viewsets.ModelViewSet,
    EnhancedResponseMixin
):
    queryset = ExchangeOrder.objects.all()
    serializer_class = ExchangeOrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieAuthentication]

    @action(detail=False, methods=['get'])
    def my_orders(self, request, pk=None):
        orders = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

