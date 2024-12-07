from rest_framework import serializers
from .models import *

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
        
    def get_images(self, obj):
        if obj.product_images:
            return [image.image.url for image in obj.product_images.all()]
        return []
        
    def create(self, validated_data):
        
        validated_data['created_by'] = self.context['request'].user
        
        return super().create(validated_data)


class UserReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display username instead of ID

    class Meta:
        model = UserReview
        fields = '__all__'


class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        
    def create(self, validated_data):
        # Extract order lines from the validated data
        order_lines_data = validated_data.pop("order_lines")
        user = self.context.get("user")

        # Create the order
        order = Order.objects.create(user=user, **validated_data)

        # Create order line items
        for line_data in order_lines_data:
            product = line_data["product"]
            if product.quantity < line_data["quantity"]:
                raise serializers.ValidationError(
                    f"Insufficient stock for product: {product.title}"
                )
            # Update product stock
            product.quantity -= line_data["quantity"]
            product.quantity_sold += line_data["quantity"]
            product.save()

            # Create OrderLine
            OrderLine.objects.create(order=order, **line_data)

        return order