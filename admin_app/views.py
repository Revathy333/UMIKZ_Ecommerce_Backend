from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from orders.models import Order
from django.db.models import Sum
from django.db.models import Q
from rest_framework import status
from products.models import Product
from .serializers import AdminProductSerializer
from django.contrib.auth.hashers import check_password
from orders.models import Order
from .serializers import AdminOrderSerializer


class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        user_count = User.objects.filter(is_staff=False).count()
        order_count = Order.objects.count()

        total_revenue = Order.objects.exclude(
            status="Cancelled"
        ).aggregate(
            Sum("total_amount")
        )["total_amount__sum"] or 0

        return Response({
            "user_count": user_count,
            "order_count": order_count,
            "total_revenue": total_revenue
        })


class AdminUserManagementView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id=None):
        if user_id:
            try:
                user = User.objects.get(id=user_id, is_staff=False)
                return Response({
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "is_active": user.is_active
                })
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        search = request.query_params.get("search", "")
        users = User.objects.filter(is_staff=False)

        if search:
            users = users.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search)
            )

        users = users.order_by("-date_joined")

        data = []
        for user in users:
            data.append({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active
            })

        return Response(data)

    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, is_staff=False)
            is_active = request.data.get("is_active")
            if is_active is not None:
                user.is_active = is_active
                user.save()
            return Response({"message": "User updated successfully"})
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, is_staff=False)
            user.delete()
            return Response({"message": "User deleted successfully"})
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        


class AdminProductManagementView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, product_id=None):
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            if not product:
                return Response(
                    {"error": "Product not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(AdminProductSerializer(product).data)

        products = Product.objects.all()

        search = request.query_params.get("search")
        category = request.query_params.get("category")

        if search:
            products = products.filter(name__icontains=search)

        if category:
            products = products.filter(category_id=category)

        products = products.order_by("-created_at")

        return Response(
            AdminProductSerializer(products, many=True).data
        )

    def post(self, request):
        serializer = AdminProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Product created successfully",
                    "product": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AdminProductSerializer(
            product, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Product updated successfully",
                    "product": serializer.data
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        product.delete()
        return Response({"message": "Product deleted successfully"})
    


class AdminOrderManagementView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, order_id=None):
        if order_id:
            order = Order.objects.filter(id=order_id).first()
            if not order:
                return Response(
                    {"error": "Order not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(AdminOrderSerializer(order).data)

        orders = Order.objects.all().order_by("-created_at")
        return Response(
            AdminOrderSerializer(orders, many=True).data
        )

    def put(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        if not order:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        status_value = request.data.get("status")

        valid_statuses = [
            "PENDING",
            "PLACED",
            "SHIPPED",
            "DELIVERED",
            "CANCELLED",
        ]

        if status_value not in valid_statuses:
            return Response(
                {"error": f"Status must be one of {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_value
        order.save()

        return Response({
            "message": "Order status updated successfully",
            "order": AdminOrderSerializer(order).data
        })



class AdminProfileUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, is_staff=True)
            
            if request.user.id != user_id:
                return Response(
                    {"error": "You can only update your own profile"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            name = request.data.get("name")
            email = request.data.get("email")
            
            if name:
                name_parts = name.split(" ", 1)
                user.first_name = name_parts[0]
                user.last_name = name_parts[1] if len(name_parts) > 1 else ""
            
            if email:
                user.email = email
            
            
            user.save()
            
            return Response({
                "message": "Profile updated successfully",
                "user": {
                    "id": user.id,
                    "name": f"{user.first_name} {user.last_name}".strip(),
                    "email": user.email,
                }
            })
            
        except User.DoesNotExist:
            return Response(
                {"error": "Admin user not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class AdminVerifyPasswordView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        password = request.data.get("password")
        
        if not password:
            return Response(
                {"error": "Password is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_valid = check_password(password, request.user.password)
        
        return Response({"valid": is_valid})


class AdminChangePasswordView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id, is_staff=True)
            
            if request.user.id != user_id:
                return Response(
                    {"error": "You can only change your own password"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            old_password = request.data.get("old_password")
            new_password = request.data.get("new_password")
            
            if not old_password or not new_password:
                return Response(
                    {"error": "Both old and new passwords are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not check_password(old_password, user.password):
                return Response(
                    {"detail": "Old password is incorrect"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(new_password)
            user.save()
            
            return Response({"message": "Password updated successfully"})
            
        except User.DoesNotExist:
            return Response(
                {"error": "Admin user not found"},
                status=status.HTTP_404_NOT_FOUND
            )