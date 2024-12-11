from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *

from dak_sih.permissions import CookieAuthentication
from dak_sih.responses import *

class ProductViewSet(
    viewsets.ModelViewSet,
    EnhancedResponseMixin
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [CookieAuthentication]
    
    def list(self, request):
        queryset = Product.objects.filter(is_active=True)  # Only fetch active products
        
        # Apply filters from query parameters
        title = request.query_params.get('title', None)
        if title:
            print(title)
            queryset = queryset.filter(title__icontains=title)
                        
        min_price = request.query_params.get('min_price', None) 
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
            
        max_price = request.query_params.get('max_price', None)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        collections = request.query_params.getlist('collection')
        if collections:
            queryset = queryset.filter(collection__slug__in=collections)
            
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(slug=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(data="Product", status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["post"])
    def addReview(self, request, pk=None):
        product = self.get_object()
        
        if not Order.objects.filter(user=request.user, order_lines__product=product).exists():
            return Response(data={"detail": "You must purchase the product before reviewing"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete"])
    def deleteReview(self, request, pk=None):
        product = self.get_object()
        review = UserReview.objects.filter(user=request.user, product=product).first()
        
        if not review:
            return Response(data="Review", status=status.HTTP_404_NOT_FOUND)
        review.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def getReviews(self, request, pk=None):
        product = self.get_object()
        reviews = UserReview.objects.filter(product=product)
        serializer = UserReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CollectionViewSet(
    viewsets.ModelViewSet,
    EnhancedResponseMixin
):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    authentication_classes = [CookieAuthentication]
    
    def list(self, request):
        collections = Collection.objects.all()  # Only fetch active products
        serializer = CollectionSerializer(collections, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO: Add retrieve method to get a single collection by slug
    def retrieve(self, request, pk=None):
        try:
            collection = Collection.objects.get(slug=pk)
        except Collection.DoesNotExist:
            return Response(data="Collection", status=status.HTTP_404_NOT_FOUND)
        
        serializer = CollectionSerializer(collection)
        
        products = collection.products.filter(is_active=True)
        product_serializer = ProductSerializer(products, many=True)
        
        return Response(data={"collection": serializer.data, "products": product_serializer.data}, status=status.HTTP_200_OK)


class OrderViewSet(
    viewsets.ModelViewSet,
    EnhancedResponseMixin
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [CookieAuthentication]
    
    def destroy(self, request, *args, **kwargs):
        return Response(data={"detail": "Order cant be deleted"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def placeOrder(self, request):
        serializer = OrderSerializer(data=request.data, context={"user": request.user})

        if serializer.is_valid():
            order = serializer.save()  # Save the order and handle line items in the serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def updateStatus(self, request, pk=None):
        order = self.get_object()
        status = request.data.get("status")
        
        if status not in [choice[0] for choice in Order.STATUS_CHOICES]:
            return Response(data={"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        if status == "cancelled":
            if order.created_at + timedelta(hours=8) < timezone.now():
                return Response(data={"detail": "Order cannot be cancelled after 8 hours"}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = status
        order.save()
        return Response(status=status.HTTP_200_OK)
