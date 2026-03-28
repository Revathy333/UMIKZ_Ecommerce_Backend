from django.urls import path
from .views import CartDetailAPIView, AddToCartAPIView
from .views import UpdateCartItemAPIView, RemoveCartItemAPIView

urlpatterns = [
    path("", CartDetailAPIView.as_view(), name="cart-detail"),
    path("add/", AddToCartAPIView.as_view(), name="cart-add"),
    path("item/<int:item_id>/", UpdateCartItemAPIView.as_view(), name="cart-update"),
    path("item/<int:item_id>/remove/", RemoveCartItemAPIView.as_view(), name="cart-remove"),


]
