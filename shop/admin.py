from django.contrib import admin
from .models import Product, Contact, Order, OrderUpdate

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_id',)

admin.site.register(Order, OrderAdmin)

# Register your models here.
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(OrderUpdate)