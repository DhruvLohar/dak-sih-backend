
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
    
    # TODO: Hide the fields which are not required to be shown
    status = serializers.HiddenField(default="Pending")
    rejection_reason = serializers.HiddenField(default=None)
    
    
    class Meta:
        model = PDA
        fields = '__all__'

    def create(self, validated_data):
        validated_data['philatelist'] = self.context['request'].user
        return super().create(validated_data)
