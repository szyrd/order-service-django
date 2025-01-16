from django.contrib import admin
from .models import Order, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'quantity')
    search_fields = ('name',)
    list_filter = ('price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'status', 'total_price', 'is_deleted')
    search_fields = ('customer_name', 'status')
    list_filter = ('status', 'is_deleted')
    filter_horizontal = ('products',)

@admin.action(description="Mark selected orders as confirmed")
def mark_as_confirmed(self, request, queryset):
    queryset.update(status='confirmed')

class OrderAdmin(admin.ModelAdmin):
    actions = [mark_as_confirmed]
