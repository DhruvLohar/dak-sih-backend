from rest_framework.decorators import action
from dak_sih.responses import *

from .models import *
from .serializers import *

class UserServicesMixin:
    
    @action(detail=False, methods=['GET'])
    def allAnnouncements(self, request):
        
        announcements = Announcement.objects.all()
        serializer = AnnouncementSerializer(announcements, many=True)
        
        return ResponseSuccess({
            "all_annoucements": serializer.data
        })
    
    @action(detail=False, methods=['GET'])
    def allNotifications(self, request):
        
        notifications = request.user.all_notifications.all()
        serializer = NotificationSerializer(notifications, many=True)
        
        return ResponseSuccess({
            "all_notifications": serializer.data
        })
    
    @action(detail=False, methods=['GET'])
    def allWorkshops(self, request):
        
        workshops = Workshop.objects.filter(for_government=False)
        serializer = WorkshopSerializer(workshops, many=True)
        
        return ResponseSuccess({
            "all_workshops": serializer.data
        })
        
    @action(detail=False, methods=['POST'])
    def workshopDetails(self, request):
        workshop_id = request.data.get("workshop_id")
        
        try:
            workshops = Workshop.objects.filter(id=workshop_id, for_government=False)
            serializer = WorkshopSerializer(workshops, many=True)
            
            return ResponseSuccess({
                "all_workshops": serializer.data
            })
        except Workshop.DoesNotExist:
            return ResponseError(message="Workshop not found")
    