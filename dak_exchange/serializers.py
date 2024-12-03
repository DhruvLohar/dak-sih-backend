from rest_framework import serializers
from .models import *

class ExchangeProductSerializer(serializers.ModelSerializer):
    # TODO: Make current_owner and previous_owners, quantity_sold, is_active, created_at, updated_at read only
    previous_owners = serializers.HiddenField(default=list())
    current_owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quantity_sold = serializers.HiddenField(default=0)
    is_active = serializers.HiddenField(default=True)
    
    class Meta:
        model = ExchangeProduct
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['current_owner'] = self.context['request'].user
        return super().create(validated_data)

class ExchangeOrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=ExchangeProduct.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = ExchangeOrder
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        
        if not validated_data['product'].is_active:
            raise serializers.ValidationError("Product is not active")
        if validated_data['product'].quantity_sold >= validated_data['product'].quantity:
            raise serializers.ValidationError("Product is out of stock")
        
        if validated_data['product'].current_owner == validated_data['user']:
            raise serializers.ValidationError("Product owner and user are the same")
        
        instance = super().create(validated_data)
        instance.product.transfer_ownership(instance.user)
        
        return instance

