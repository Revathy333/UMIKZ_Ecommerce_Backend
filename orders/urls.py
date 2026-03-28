from django.urls import path
from .views import PlaceOrderAPIView,OrderListAPIView

urlpatterns = [
    path("place/", PlaceOrderAPIView.as_view(), name="place-order"),
    path("", OrderListAPIView.as_view(), name="order-list"),
]
