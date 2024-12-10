from rest_framework import serializers
from .models import *

class BlogSerializer(serializers.ModelSerializer):
    
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = '__all__'
        
    def get_author(self, obj):
        return {
            "name": obj.user.name,
            "email": obj.user.email,
            "profile_picture": obj.user.profile_img.url if obj.user.profile_img else None
        }
        
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
