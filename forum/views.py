from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *

from dak_sih.responses import EnhancedResponseMixin
from dak_sih.permissions import CookieAuthentication

class ForumPostViewSet(
    viewsets.ModelViewSet,
    EnhancedResponseMixin
):
    queryset = ForumPost.objects.filter(is_active=True)
    serializer_class = ForumPostSerializer
    permission_classes = [IsAuthenticated] # kon aa sakta hai
    authentication_classes = [CookieAuthentication] # jo aara woh kon hai
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes_count += 1
        post.save()
        
        return Response(data={
            "likes_count": post.likes_count
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        if post.likes_count > 0:
            post.likes_count -= 1
            post.save()
            
        return Response(data={
            "likes_count": post.likes_count
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        post = self.get_object()
        replies = ForumPostReply.objects.filter(post=post, is_active=True)
        serializer = ForumPostReplySerializer(replies, many=True)
        
        return Response(data={
            "replies": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_reply(self, request, pk=None):
        post = self.get_object()
        serializer = ForumPostReplySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
                post=post,
                user=request.user
            )
            return Response(data={
                "reply": serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(data={
            "detail": str(serializer.error_messages)    
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def delete_reply(self, request, pk=None):
        post = self.get_object()
        reply_id = request.data.get("reply_id")
        
        try:
            reply = ForumPostReply.objects.get(id=reply_id, post=post)
            if (request.user.id == reply.user.id) or (request.user.id == post.user.id):
                reply.is_active = False
                reply.save()

                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except ForumPostReply.DoesNotExist:
            return Response(data="ForumPost", status=status.HTTP_404_NOT_FOUND)