# TODO: Add views for PostalOffice and AdminUser
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import PostalOffice, AdminUser
from .serializers import PostalOfficeSerializer, AdminUserSerializer

from dak_sih.permissions import CookieAuthentication
from dak_sih.responses import EnhancedResponseMixin

class PostalOfficeViewSet(EnhancedResponseMixin, viewsets.ModelViewSet):
    queryset = PostalOffice.objects.all()
    serializer_class = PostalOfficeSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [CookieAuthentication]

class AdminUserViewSet(EnhancedResponseMixin, viewsets.ModelViewSet):
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [CookieAuthentication]
    

