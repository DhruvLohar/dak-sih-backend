
from rest_framework import serializers
from .models import *

class PostalOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalOffice
        fields = '__all__'
    
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = '__all__'

class PDAUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDA
        fields = '__all__'

