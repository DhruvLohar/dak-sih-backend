from rest_framework import serializers
from .models import *

class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = '__all__'
        
class AnnouncementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Announcement
        fields = '__all__'
