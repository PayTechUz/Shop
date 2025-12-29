from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Order

# Register your models here.


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'product_name', 'amount', 'status', 'payment_type', 'created_at')
    list_filter = ('status', 'payment_type', 'created_at')
    search_fields = ('id', 'product_name')
