from rest_framework import serializers
from .models import Philatelist

class PhilatelistSerializer(serializers.ModelSerializer):
    
    profile_img = serializers.SerializerMethodField()
    
    class Meta:
        model = Philatelist
        exclude = (
            'access_token', 'valid_otp', 'is_active',
        )
        
    def get_profile_img(self, instance):
        request = self.context.get("request")
        return request.build_absolute_uri(instance.profile_img.url) if instance.profile_img and request else None   

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Philatelist
        fields = ['name', 'email']