from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

class SuperAdminMixin:
    def has_permission(self, request, view):
        # Allow all non-action methods
        if not hasattr(view, 'action'):
            return True
            
        # For actions, check if user is super admin
        return request.user and request.user.is_super_admin
    
    def has_object_permission(self, request, view, obj):
        # Allow all non-action methods
        if not hasattr(view, 'action'):
            return True
            
        # For actions, check if user is super admin
        return request.user and request.user.is_super_admin
    
    # TODO: Add custom actions for adding users (name, email)
    @action(detail=False, methods=['POST'])
    def addUser(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        
        serializer = AdminUserSerializer(data={
            'name': name,
            'email': email,
            'is_super_admin': False
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    # TODO: 
