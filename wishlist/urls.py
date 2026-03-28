from django.urls import path
from .views import (
    WishlistDetailAPIView,
    WishlistAddAPIView,
    WishlistRemoveAPIView,
    ClearWishlistAPIView
)

urlpatterns = [
    path("", WishlistDetailAPIView.as_view(), name="wishlist-detail"),
    path("add/", WishlistAddAPIView.as_view(), name="wishlist-add"),
    path("remove/<int:product_id>/", WishlistRemoveAPIView.as_view(), name="wishlist-remove"),
    path("clear/", ClearWishlistAPIView.as_view(), name="wishlist-clear"),
]
