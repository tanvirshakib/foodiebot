# admin.py

from django.contrib import admin
from .models import MyUser, CustomerOrder, Reservation, Category, MenuItem

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'name', 'is_admin', 'is_staff')
    search_fields = ('username', 'phone_number', 'name')
    list_filter = ('is_admin', 'is_staff')

@admin.register(CustomerOrder)
class CustomerOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'delivery_preference', 'subtotal', 'sales_tax', 'grand_total', 'order_date')
    search_fields = ('user__username', 'delivery_preference')
    list_filter = ('order_date', 'delivery_preference')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'num_of_people')
    search_fields = ('user__username', 'date')
    list_filter = ('date',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)



