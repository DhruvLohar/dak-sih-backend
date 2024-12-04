from random import randint
from rest_framework import viewsets, status
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.utils import html
from django.template.loader import render_to_string
from rest_framework.permissions import IsAuthenticated

from dak_sih import settings
from dak_sih.permissions import CookieAuthentication
from dak_sih.responses import EnhancedResponseMixin

from philatelist.models import Philatelist
from philatelist.serializers import *

from dashboard.serializers import PDAUserSerializer

from services.views import UserServicesMixin

class AuthMixin:
    
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
    def getOTPOnEmail(self, request, pk=None):
        uid = request.data.get("uid")
        
        try:
            user = Philatelist.objects.get(id=uid)
            
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
            return Response(data={"detail": "Something went wrong sending the email"}, status=status.HTTP_417_EXPECTATION_FAILED)
        except Philatelist.DoesNotExist:
            return Response(data="Philatelist", status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['POST'], permission_classes=[])
    def verifyOTPOnEmail(self, request, pk=None):
        uid = request.data.get("uid")
        entered_otp = request.data.get("otp")
        
        try:
            user = Philatelist.objects.get(id=uid)
            
            if user.valid_otp == int(entered_otp):
                accessToken, changeUserToken = user.generateToken()
                if changeUserToken:
                    user.access_token = accessToken

                user.is_active = True
                user.last_login = timezone.now()
                user.save()
                
                return Response(data={
                    "verified": True,
                    "id": user.id,
                    "email": user.email,
                    "phone_number": user.phone_number,
                    "name": user.name,
                    "profile_img": user.profile_img,
                    "access_token": user.access_token
                }, status=status.HTTP_200_OK)
            return Response(data={"detail": "Invalid OTP. Please try again"}, status=status.HTTP_400_BAD_REQUEST)
        except Philatelist.DoesNotExist:
            return Response(data="Philatelist", status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['POST'], permission_classes=[])
    def signUpSignIn(self, request):
        email = request.data.get("email")
        
        try:
            user = Philatelist.objects.get(email=email)
            
            return Response(data={
                "id": user.id,
                "verified": user.is_active,
            }, status=status.HTTP_200_OK)
        except Philatelist.DoesNotExist:
            try:
                with transaction.atomic():
                    serializer = CreateUserSerializer(data=request.data)
                    
                    if serializer.is_valid(raise_exception=False):
                        serializer.save()
                        
                        user = Philatelist.objects.get(email=serializer.data.get("email"))
                        user.is_active = False
                        user.save()
                    
                        return Response(data={
                            "id": user.id,
                            "verified": False,
                        }, status=status.HTTP_200_OK)
                    
                    if serializer.errors.get("email"):
                        return Response(
                            data={"detail": "User with the same 'email' already exists"},
                            status=status.HTTP_400_BAD_REQUEST
                        )    
                    
                    return Response(
                        {"detail": str(serializer.error_messages)},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
            except IntegrityError:
                return Response(
                    data={"detail": "User with the same 'email' already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )  
            except UnicodeDecodeError as e:
                return Response(
                    data={"detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )  
            except Exception as e:
                return Response(
                    data={"detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )  
                
            
class PhilatelistAPIView(
    AuthMixin,
    UserServicesMixin,
    viewsets.ModelViewSet,
    EnhancedResponseMixin
):
    queryset = Philatelist.objects.all()
    serializer_class = PhilatelistSerializer
    permission_classes = [IsAuthenticated] # kon aa sakta hai
    authentication_classes = [CookieAuthentication] # jo aara woh kon hai

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
        
    @action(detail=False, methods=['GET'])
    def getProfile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def getPDAProfile(self, request):
        serializer = PDAUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['POST'])
    def createPDAProfile(self, request):
        serializer = PDAUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    