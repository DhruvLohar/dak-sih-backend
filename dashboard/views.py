from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.utils import html
from django.template.loader import render_to_string
from random import randint
from dak_sih import settings

from .models import *
from .serializers import *

from store.models import *
from store.serializers import *

from services.models import *
from services.serializers import *

from dak_sih.permissions import CookieAuthentication
from dak_sih.responses import EnhancedResponseMixin

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and isinstance(request.user, AdminUser)

class AdminUserViewSet(EnhancedResponseMixin, viewsets.ViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [CookieAuthentication]
    
    @staticmethod
    def send_otp_on_email(subject, template_name, email_to, context=None):
        try:
            email_template = render_to_string(template_name, context=context if context else {})
            template_content = html.strip_tags(email_template)
            email = EmailMultiAlternatives(subject, template_content, settings.EMAIL_HOST_USER, to=[email_to])
            email.attach_alternative(email_template, 'text/html')
            email.send()
            return True
        except Exception as e:
            print(e)
            return False
    
    @action(detail=False, methods=['POST'], permission_classes=[])
    def verifyOTP(self, request):
        uid = request.data.get("uid")
        entered_otp = request.data.get("otp")
        
        try:
            user = AdminUser.objects.get(id=uid)
            
            if user.valid_otp == int(entered_otp):
                accessToken, changeUserToken = user.generateToken()
                if changeUserToken:
                    user.access_token = accessToken

                user.is_active = True
                user.last_login = timezone.now()
                user.save()
                
                return Response(data={
                    "id": user.id,
                    "email": user.email,
                    "access_token": user.access_token
                }, status=status.HTTP_200_OK)
            return Response(data={"detail": "Invalid OTP. Please try again"}, status=status.HTTP_400_BAD_REQUEST)
        except AdminUser.DoesNotExist:
            return Response(data="Admin User", status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['POST'], permission_classes=[])
    def login(self, request):
        email = request.data.get("email")
        
        try:
            user = AdminUser.objects.get(email=email)
            
            generated_otp = randint(10000, 99999)
            email_sent = self.send_otp_on_email(
                "Dak | OTP Authentication",
                "otp_email_template.html",
                user.email,
                context={
                    "date": timezone.now().strftime("%d %B, %Y"),
                    "username": user.name,
                    "generated_otp": generated_otp
                }
            )
            
            if email_sent:
                user.valid_otp = generated_otp
                user.save()
                return Response(
                    data="Email was sent on the specified email",
                    status=status.HTTP_200_OK
                )
            
            return Response(data={
                "id": user.id,
            }, status=status.HTTP_200_OK)
        except AdminUser.DoesNotExist:
            return Response(
                data={"detail": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )  
    
    @action(detail=False, methods=['POST'])
    def addProduct(self, request):
        serializer = ProductSerializer(data=request.data, context={'request': request})
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

    @action(detail=False, methods=['POST'])
    def updatePDAStatus(self, request):
        pid = request.data.get('pid')
        status = request.data.get('status')
        reason = request.data.get('reason')
        
        try:
            pda = PDA.objects.get(id=pid)
        except PDA.DoesNotExist:
            return Response(data="PDA Application", status=status.HTTP_404_NOT_FOUND)
        
        if status != "Pending":
            pda.status = status
            if status == "Rejected":
                pda.rejection_reason = reason
            pda.save()
            return Response(status=status.HTTP_200_OK)
        
        return Response(data={"detail": "Status cannot be updated"}, status=status.HTTP_400_BAD_REQUEST)


