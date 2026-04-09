from django.urls import path

from . import views

app_name = "restaurant"

urlpatterns = [
    path("", views.home, name="home"),
    path("restaurant/<int:pk>/", views.restaurant_detail, name="detail"),
    path("owner/restaurant/", views.my_restaurant, name="my_restaurant"),
    path("owner/menu/", views.menu_manage, name="menu_manage"),
    path("owner/menu/add/", views.menu_item_create, name="menu_item_create"),
    path("owner/menu/<int:pk>/edit/", views.menu_item_edit, name="menu_item_edit"),
    path("owner/menu/<int:pk>/delete/", views.menu_item_delete, name="menu_item_delete"),
]
