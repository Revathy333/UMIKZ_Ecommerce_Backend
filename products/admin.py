from django.contrib import admin

# Register your models here.

from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "offer_price", "category", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "category")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("name",)
    search_fields = ("name",)    
