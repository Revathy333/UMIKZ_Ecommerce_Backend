# In orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import Cart
from decimal import Decimal


# class OrderItemSerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(source='product.name', read_only=True)
#     product_image = serializers.ImageField(source='product.image', read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ['id', 'product', 'product_name', 'product_image', 'quantity', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.SerializerMethodField()
    category_name = serializers.CharField(
        source='product.category.name',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_image',
            'category_name',
            'quantity',
            'price'
        ]

    def get_product_image(self, obj):
        if obj.product.image:
            return obj.product.image.url
        return None



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 
            'status', 
            'created_at', 
            'shipping_address', 
            'phone', 
            'payment_method',
            'total_amount',
            'items'
        ]
        read_only_fields = ['id', 'created_at', 'total_amount', 'items']
    
    def create(self, validated_data):
        user = validated_data.pop('user')
        status = validated_data.pop('status')
        
        cart = Cart.objects.get(user=user)
        
        total_amount = Decimal('0.00')
        for cart_item in cart.items.all():
            price = cart_item.product.offer_price if hasattr(cart_item.product, 'offer_price') and cart_item.product.offer_price else cart_item.product.price
            total_amount += price * cart_item.quantity
        
        order = Order.objects.create(
            user=user,
            status=status,
            total_amount=total_amount,
            **validated_data
        )
        
        for cart_item in cart.items.all():
            price = cart_item.product.offer_price if hasattr(cart_item.product, 'offer_price') and cart_item.product.offer_price else cart_item.product.price
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=price
            )
        
        cart.items.all().delete()
        
        return order