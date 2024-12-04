from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

from dak_sih.responses import *
from dak_sih.permissions import CookieAuthentication

class UserServicesMixin:
    
    @action(detail=False, methods=['GET'])
    def allAnnouncements(self, request):
        
        announcements = Announcement.objects.all()
        serializer = AnnouncementSerializer(announcements, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def allNotifications(self, request):
        
        notifications = request.user.all_notifications.all()
        serializer = NotificationSerializer(notifications, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
        
    @action(detail=False, methods=['GET'])
    def allCatalog(self, request):
        
        catalog = Catalog.objects.all()
        serializer = CatalogSerializer(catalog, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['POST'])
    def catalogDetails(self, request):
        
        catalog_id = request.data.get("catalog_id")
        
        try:
            catalog = Catalog.objects.get(id=catalog_id)
            serializer = CatalogSerializer(catalog)
            
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Catalog.DoesNotExist:
            return Response(data="Catalog", status=status.HTTP_404_NOT_FOUND)


class BlogViewSet(ModelViewSet, EnhancedResponseMixin):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieAuthentication]

