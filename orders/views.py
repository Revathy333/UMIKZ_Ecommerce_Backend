from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from decimal import Decimal

from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem
from products.models import Product


class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        shipping_address = request.data.get('shipping_address')
        phone = request.data.get('phone')
        payment_method = request.data.get('payment_method', 'cod').lower()

        if not shipping_address:
            return Response(
                {"error": "Shipping address is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not phone:
            return Response(
                {"error": "Phone number is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if payment_method not in ['cod', 'online']:
            return Response(
                {"error": "Invalid payment method"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if product_id and quantity:
            return self._handle_direct_purchase(
                request.user,
                product_id,
                quantity,
                shipping_address,
                phone,
                payment_method
            )
        else:
            return self._handle_cart_order(
                request.user,
                shipping_address,
                phone,
                payment_method
            )

    def _handle_direct_purchase(self, user, product_id, quantity, shipping_address, phone, payment_method):
        """Handle Buy Now - direct product purchase"""
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found or unavailable"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST
            )

        price = product.offer_price if product.offer_price else product.price
        total_amount = Decimal(str(price)) * quantity

        order = Order.objects.create(
            user=user,
            status='PLACED',
            shipping_address=shipping_address,
            phone=phone,
            payment_method=payment_method,
            total_amount=total_amount
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price
        )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _handle_cart_order(self, user, shipping_address, phone, payment_method):
        """Handle cart-based order (existing functionality)"""
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response(
                {"error": "No cart found for user"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not cart.items.exists():
            return Response(
                {"error": "Your cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = Decimal('0.00')
        for cart_item in cart.items.all():
            price = cart_item.product.offer_price if cart_item.product.offer_price else cart_item.product.price
            total_amount += Decimal(str(price)) * cart_item.quantity

        order = Order.objects.create(
            user=user,
            status='PLACED',
            shipping_address=shipping_address,
            phone=phone,
            payment_method=payment_method,
            total_amount=total_amount
        )

        for cart_item in cart.items.all():
            price = cart_item.product.offer_price if cart_item.product.offer_price else cart_item.product.price
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=price
            )

        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)