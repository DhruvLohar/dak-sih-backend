from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

from store.models import *
from store.serializers import *

from services.models import *
from services.serializers import *

from dak_sih.permissions import CookieAuthentication
from dak_sih.responses import EnhancedResponseMixin

class AdminUserViewSet(EnhancedResponseMixin, viewsets.ViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [CookieAuthentication]
    
    @action(detail=False, methods=['POST'])
    def addProduct(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['PATCH'])
    def updateProduct(self, request):
        pid = request.data.get('pid')
        
        try:    
            product = Product.objects.get(id=pid)
        except Product.DoesNotExist:
            return Response(data="Product", status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['DELETE'])
    def deleteProduct(self, request):
        pid = request.data.get('pid')
        
        try:
            product = Product.objects.get(id=pid)
        except Product.DoesNotExist:
            return Response(data="Product", status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['POST'])
    def addCollection(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['PATCH'])
    def updateCollection(self, request):
        cid = request.data.get('cid')
        
        try:
            collection = Collection.objects.get(id=cid)
        except Collection.DoesNotExist:
            return Response(data="Collection", status=status.HTTP_404_NOT_FOUND)
        
        serializer = CollectionSerializer(collection, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['DELETE'])
    def deleteCollection(self, request):
        cid = request.data.get('cid')
        
        try:
            collection = Collection.objects.get(id=cid)
        except Collection.DoesNotExist:
            return Response(data="Collection", status=status.HTTP_404_NOT_FOUND)
        
        collection.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST'])
    def addAccountment(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
