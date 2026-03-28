from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "items", "created_at")


class CartItemMiniSerializer(serializers.ModelSerializer):
    cart_item_id = serializers.IntegerField(source="id")
    product_id = serializers.IntegerField(source="product.id")
    name = serializers.CharField(source="product.name")
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            "cart_item_id",
            "product_id",
            "name",
            "image",
            "price",
            "quantity",
            "subtotal",
        )

    def get_image(self, obj):
        return obj.product.image.url if obj.product.image else None

    def get_price(self, obj):
        return obj.product.offer_price or obj.product.price

    def get_subtotal(self, obj):
        price = obj.product.offer_price or obj.product.price
        return obj.quantity * price


class CartMiniSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source="id")
    items = CartItemMiniSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            "cart_id",
            "items",
            "total_items",
            "total_price",
        )

    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.items.all())

    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            price = item.product.offer_price or item.product.price
            total += item.quantity * price
        return total



