from rest_framework import serializers
from .models import *

class BlogSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Blog
        fields = '__all__'
        
    def create(self, validated_data):
        
        validated_data['user'] = self.context['request'].user
        
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = '__all__'

        
class AnnouncementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Announcement
        fields = '__all__'


class CatalogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Catalog
        fields = '__all__'
