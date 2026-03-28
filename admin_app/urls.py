from django.urls import path
from .views import AdminDashboardView,AdminUserManagementView
from .views import AdminProductManagementView,AdminOrderManagementView
from .views import AdminProfileUpdateView,AdminVerifyPasswordView,AdminChangePasswordView

urlpatterns = [
    path("dashboard/", AdminDashboardView.as_view()),
    path("users/", AdminUserManagementView.as_view()),
    path("users/<int:user_id>/", AdminUserManagementView.as_view()),
    path("products/", AdminProductManagementView.as_view()),
    path("products/<int:product_id>/", AdminProductManagementView.as_view()),  
    path("orders/", AdminOrderManagementView.as_view()),
    path("orders/<int:order_id>/", AdminOrderManagementView.as_view()),   
    path("profile/<int:user_id>/", AdminProfileUpdateView.as_view()),
    path("verify-password/", AdminVerifyPasswordView.as_view()),
    path("change-password/<int:user_id>/", AdminChangePasswordView.as_view()),

]
