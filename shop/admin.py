from django.contrib import admin
from .models import Blog
from .models import OrderItem
from .models import (
    Product, Category, AdminProfile, Profile, Cart,
    ShippingOption, Wishlist, Order, Review
)

@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin_title')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'availability','best_deal')
    list_filter = ('availability', 'best_deal', 'category')  # Allow filter by best_deal
    list_editable = ('best_deal',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'gender')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')

@admin.register(ShippingOption)
class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'note')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_list', 'total_quantity', 'status', 'payment_option', 'order_date')

    def product_list(self, obj):
        return ", ".join([item.product.name for item in obj.items.all()])
    product_list.short_description = 'Products'

    def total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())
    total_quantity.short_description = 'Total Qty'



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)
    list_filter = ('date',)
