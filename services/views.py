import os
import uuid

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

from dak_sih.responses import *
from dak_sih.permissions import CookieAuthentication

from .tasks import *

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


class MLServiceMixin:
    @action(detail=False, methods=['POST'])
    def stampVision(self, request):
        image_file = request.data.get("image")
        if not image_file:
            return Response(
                {"error": "No image provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create images directory if it doesn't exist
        os.makedirs("./images", exist_ok=True)
        
        # Generate unique filename
        filename = f"stamp_{str(uuid.uuid4())}.png"
        image_path = os.path.join("./images", filename)
        
        # Save uploaded image
        with open(image_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)
        
        response = stamp_vision_response.delay(image_path)
        return Response(data=response.get(), status=status.HTTP_200_OK)
