from rest_framework import serializers
from .models import *
from philatelist.models import Philatelist

# Serializer for ForumPostReply
class ForumPostReplySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name')

    class Meta:
        model = ForumPostReply
        fields = ['user', 'content', 'created_at', 'is_active']

class ForumPostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPostImage
        fields = ['id', 'image']

class ForumPostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)  # Ensure it's read-only
    replies = ForumPostReplySerializer(many=True, read_only=True)
    post_images = serializers.SerializerMethodField()  # Use SerializerMethodField for read functionality
    uploaded_images = serializers.ListField(  # Separate field for uploads
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    is_active = serializers.BooleanField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ForumPost
        fields = ['user', 'content', 'created_at', 'updated_at', 'is_active', 'likes_count', 'replies', 'post_images', 'uploaded_images']
        
        
    def get_post_images(self, instance: ForumPost):
        images = instance.post_images.all()
        serializer = ForumPostImageSerializer(images, many=True)
        return serializer.data

    def create(self, validated_data):
        uploaded_images = self.context.get('images', [])
        
        # Ensure the authenticated user is linked to the post
        user = self.context['user']
        validated_data['user'] = user
        
        forum_post = ForumPost.objects.create(**validated_data)

        # Handle the related images
        for image in uploaded_images:
            ForumPostImage.objects.create(post=forum_post, image=image)

        return forum_post
    
    def update(self, instance, validated_data):
        validated_data.pop('likes_count', None)
        validated_data.pop('is_active', None)

        # Call the parent update method with the remaining fields
        return super().update(instance, validated_data)