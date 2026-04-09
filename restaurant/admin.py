from django.contrib import admin

from .models import MenuItem, Restaurant


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_active", "created_at")
    list_filter = ("is_active",)
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price", "is_available")
    list_filter = ("is_available", "restaurant")
