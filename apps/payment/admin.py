from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Invoice

# Register your models here.


@admin.register(Invoice)
class InvoiceAdmin(ModelAdmin):
    list_display = ('id', 'order', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'order__id')
