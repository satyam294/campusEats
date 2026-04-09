from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:menu_item_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/clear/", views.clear_cart, name="clear_cart"),
    path("cart/item/<int:pk>/update/", views.update_cart_item, name="update_cart_item"),
    path("cart/item/<int:pk>/remove/", views.remove_cart_item, name="remove_cart_item"),
    path("checkout/", views.checkout, name="checkout"),
    path("mine/", views.my_orders, name="mine"),
    path("<int:pk>/", views.order_detail, name="detail"),
    path("<int:pk>/status/", views.owner_update_status, name="owner_update_status"),
]
