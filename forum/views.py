from rest_framework import viewsets, status
from rest_framework.decorators import action

from .models import *
from .serializers import *

from dak_sih.responses import *
from dak_sih.permissions import CookieAuthentication

class ForumPostViewSet(viewsets.ModelViewSet):
    queryset = ForumPost.objects.filter(is_active=True)
    serializer_class = ForumPostSerializer
    authentication_classes = [CookieAuthentication]

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes_count += 1
        post.save()
        
        return ResponseSuccess({
            "likes_count": post.likes_count
        })

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()
        if post.likes_count > 0:
            post.likes_count -= 1
            post.save()
            
        return ResponseSuccess({
            "likes_count": post.likes_count
        })

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        post = self.get_object()
        replies = ForumPostReply.objects.filter(post=post, is_active=True)
        serializer = ForumPostReplySerializer(replies, many=True)
        
        return ResponseSuccess({
            "replies": serializer.data
        })

    @action(detail=True, methods=['post'])
    def add_reply(self, request, pk=None):
        post = self.get_object()
        serializer = ForumPostReplySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(
                post=post,
                user=request.user
            )
            return ResponseSuccess({
                "reply": serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def delete_reply(self, request, pk=None):
        post = self.get_object()
        reply_id = request.data.get("reply_id")
        
        try:
            reply = ForumPostReply.objects.get(id=reply_id, post=post)
            if (request.user.id == reply.user.id) or (request.user.id == post.user.id):
                reply.is_active = False
                reply.save()

                return ResponseSuccess(message="Post Reply was deleted")
            return ResponseError(message="Unauthorized Request")
        except ForumPostReply.DoesNotExist:
            return ResponseError(message="Reply not found")
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if request.user.id == instance.user.id:
            instance.is_active = False
            instance.save()

            return ResponseSuccess(message="Post was deleted")
        return ResponseError(message="Unauthorized Request")