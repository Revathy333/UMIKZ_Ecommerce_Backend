from rest_framework import serializers
from products.models import Product, Category
from orders.models import Order,OrderItem
from django.conf import settings


class AdminProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "offer_price",
            "image",
            "category",
            "is_active",
            "created_at",
        ]
    
    def get_image(self, obj):
        if obj.image:
            if str(obj.image).startswith('http'):
                return str(obj.image)
            cloud_name = getattr(settings, 'CLOUDINARY_STORAGE', {}).get('CLOUD_NAME')
            return f"https://res.cloudinary.com/{cloud_name}/{obj.image}"
        return None
    
    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if 'image' in self.initial_data:
            ret['image'] = self.initial_data['image']
        return ret
    
    # to_internal_value() is the method that converts raw request data into a Python dictionary (validated_data).
    # This method runs before:
    #validate()
    #create()
    #update()

    # This code ensures the image field is explicitly included in the validated data 
    # so it can be used during object creation or updates, 
    # even if the serializer would normally exclude it.
    # Common Use Case
    # This pattern is often used when you want an image field that's normally read-only to be writable during 
    # specific operations (like creating or updating an object with an uploaded image file).
    
    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AdminOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name", read_only=True
    )
    category_name = serializers.CharField(
        source="product.category.name", read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "category_name", 
            "price",
            "quantity",
        ]


class AdminOrderSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(
        source="user.email", read_only=True
    )
    items = AdminOrderItemSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "user_email",
            "status",
            "payment_method",
            "total_amount",
            "shipping_address",
            "phone",
            "created_at",
            "items",
        ]

