from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'payment_method', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)


