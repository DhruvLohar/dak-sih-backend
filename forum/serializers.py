from rest_framework import serializers
from .models import ForumPost, ForumPostReply
from philatelist.models import Philatelist

# Serializer for ForumPostReply
class ForumPostReplySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name')

    class Meta:
        model = ForumPostReply
        fields = ['user', 'content', 'created_at', 'is_active']
        
# Serializer for ForumPost
class ForumPostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name')  # Show username instead of user ID
    replies = ForumPostReplySerializer(many=True, read_only=True)
    
    class Meta:
        model = ForumPost
        fields = ['user', 'content', 'created_at', 'updated_at', 'is_active', 'likes_count', 'replies']
