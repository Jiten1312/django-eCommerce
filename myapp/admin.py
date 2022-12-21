from django.contrib import admin, messages
from .models import Product, Category, Client, Order, Course, Center

# Register your models here.
# admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Course)
admin.site.register(Center)


# Feature3
def refill(modelAdmin, request, querySet):
    for product in querySet:
        if product.stock+50 >1000:
            messages.error(request, 'Ensure that stock is less than or equal to 1000.')
        else:
            product.refill()


# Feature1
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available')
    actions = [refill]


admin.site.register(Product, ProductAdmin)


# Feature1
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'interests')


admin.site.register(Client, ClientAdmin)
