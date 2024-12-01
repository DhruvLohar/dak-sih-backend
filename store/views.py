from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializers import *

from dak_sih.permissions import CookieAuthentication
from dak_sih.responses import *

class ProductViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [CookieAuthentication]
    
    def list(self, request):
        products = Product.objects.filter(is_active=True)  # Only fetch active products
        serializer = ProductSerializer(products, many=True)
        
        return ResponseSuccess({
            "products": serializer.data
        })

    def retrieve(self, request, pk=None):
        product = self.get_object()
        serializer = ProductSerializer(product)
        
        return ResponseSuccess({
            "product": serializer.data
        })

    @action(detail=True, methods=["post"])
    def addReview(self, request, pk=None):
        product = self.get_object()
        if not Order.objects.filter(user=request.user, order_lines__product=product).exists():
            return ResponseError(message="You must purchase the product before reviewing")
        
        serializer = UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return ResponseSuccess(response={"review": serializer.data}, message="Review added successfully")
        return ResponseError(message=serializer.errors)

    @action(detail=True, methods=["delete"])
    def deleteReview(self, request, pk=None):
        product = self.get_object()
        review = UserReview.objects.filter(user=request.user, product=product).first()
        if not review:
            return ResponseError(message="Review not found")
        review.delete()
        return ResponseSuccess(message="Review deleted successfully")

    @action(detail=True, methods=["get"])
    def getReviews(self, request, pk=None):
        product = self.get_object()
        reviews = UserReview.objects.filter(product=product)
        serializer = UserReviewSerializer(reviews, many=True)
        return ResponseSuccess(response={"reviews": serializer.data}, message="Reviews fetched successfully")


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    authentication_classes = [CookieAuthentication]
    
    def list(self, request):
        products = Product.objects.filter(is_active=True)  # Only fetch active products
        serializer = ProductSerializer(products, many=True)
        
        return ResponseSuccess({
            "products": serializer.data
        })

    def retrieve(self, request, pk=None):
        product = self.get_object()
        serializer = ProductSerializer(product)
        
        return ResponseSuccess({
            "product": serializer.data
        })


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [CookieAuthentication]
    
    def destroy(self, request, *args, **kwargs):
        return ResponseSuccess(message="Order cant be deleted")

    @action(detail=False, methods=["post"])
    def placeOrder(self, request):
        data = request.data.copy()
        data["user"] = request.data.id

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()  # Save the order and handle line items in the serializer
            return ResponseSuccess({
                "order": serializer.data,
            })

        return ResponseError(message=f"{serializer.error_messages}")

    @action(detail=True, methods=["patch"])
    def updateStatus(self, request, pk=None):
        order = self.get_object()
        status = request.data.get("status")
        
        if status not in [choice[0] for choice in Order.STATUS_CHOICES]:
            return ResponseError(message="Invalid status")
        
        order.status = status
        order.save()
        return ResponseSuccess(message=f"Order status updated to {status}")
