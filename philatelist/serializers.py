from rest_framework import serializers
from .models import Philatelist

class PhilatelistSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Philatelist
        exclude = (
            'access_token', 'valid_otp', 'is_active', 'password'
        )
        

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Philatelist
        fields = ['name', 'email']