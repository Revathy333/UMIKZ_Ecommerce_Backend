from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PLACED", "Placed"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PLACED"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    shipping_address = models.TextField(
        help_text="Full shipping address including house number, street, city, state, pin code"
    )
    phone = models.CharField(
        max_length=15,
        help_text="Contact phone number for delivery"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[("cod", "Cash on Delivery"), ("online", "Online Payment")],
        default="cod"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Total order amount including all items and any fees"
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"