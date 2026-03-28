from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Wishlist
from .serializers import WishlistSerializer
from products.models import Product


class WishlistDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)


class WishlistAddAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {"error": "product_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found or inactive"},
                status=status.HTTP_404_NOT_FOUND
            )

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.add(product)

        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WishlistRemoveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            product = Product.objects.get(id=product_id)
        except (Wishlist.DoesNotExist, Product.DoesNotExist):
            return Response(
                {"error": "Wishlist or product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        wishlist.products.remove(product)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)
    

class ClearWishlistAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.products.clear()   
        return Response(
            {"message": "Wishlist cleared"},
            status=status.HTTP_204_NO_CONTENT
        )    

