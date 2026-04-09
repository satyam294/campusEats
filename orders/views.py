from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import Profile
from restaurant.models import MenuItem

from .models import Cart, CartItem, Order, OrderItem


def customer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        profile = getattr(request.user, "profile", None)
        if not profile or profile.role != Profile.Role.CUSTOMER:
            messages.error(
                request,
                "The cart is for food-ordering accounts. Log in with that role or create a new account to order.",
            )
            return redirect("restaurant:home")
        return view_func(request, *args, **kwargs)

    return wrapper


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
@customer_required
@require_http_methods(["POST"])
def add_to_cart(request, menu_item_id):
    item = get_object_or_404(MenuItem, pk=menu_item_id, is_available=True)
    cart = get_or_create_cart(request.user)
    ci, created = CartItem.objects.get_or_create(cart=cart, menu_item=item, defaults={"quantity": 1})
    if not created:
        ci.quantity += 1
        ci.save()

    # Check if this is an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Calculate cart count after adding the item
        cart_count = sum(ci.quantity for ci in cart.items.all())
        return JsonResponse({
            'success': True,
            'message': f"Nice choice — {item.name} is in your cart.",
            'cart_count': cart_count
        })

    # For regular form submissions, redirect back to referring page
    messages.success(request, f"Nice choice — {item.name} is in your cart.")
    referer = request.META.get('HTTP_REFERER')
    if referer and 'restaurant' in referer:
        return redirect(referer)
    return redirect("restaurant:home")


@login_required
@customer_required
@require_http_methods(["POST"])
def clear_cart(request):
    cart = getattr(request.user, "cart", None)
    if cart:
        cart.items.all().delete()
        messages.info(request, "Cart emptied — ready for a fresh order.")
    return redirect("orders:cart")


@login_required
@customer_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related("menu_item", "menu_item__restaurant")
    return render(
        request,
        "orders/cart.html",
        {"cart": cart, "items": items, "total": cart.total()},
    )


@login_required
@customer_required
@require_http_methods(["POST"])
def update_cart_item(request, pk):
    cart = get_or_create_cart(request.user)
    ci = get_object_or_404(CartItem, pk=pk, cart=cart)
    qty = int(request.POST.get("quantity", 1))
    if qty < 1:
        ci.delete()
        messages.info(request, "Removed from your cart.")
    else:
        ci.quantity = qty
        ci.save()
        messages.success(request, "Quantities saved.")
    return redirect("orders:cart")


@login_required
@customer_required
@require_http_methods(["POST"])
def remove_cart_item(request, pk):
    cart = get_or_create_cart(request.user)
    ci = get_object_or_404(CartItem, pk=pk, cart=cart)
    ci.delete()
    messages.info(request, "That item’s been removed.")
    return redirect("orders:cart")


@login_required
@customer_required
@require_http_methods(["GET", "POST"])
def checkout(request):
    cart = get_or_create_cart(request.user)
    items = list(cart.items.select_related("menu_item", "menu_item__restaurant"))
    if not items:
        messages.warning(request, "Your cart is empty — add something delicious first.")
        return redirect("orders:cart")
    restaurant_ids = {i.menu_item.restaurant_id for i in items}
    multiple_restaurants = len(restaurant_ids) > 1
    restaurant = items[0].menu_item.restaurant if not multiple_restaurants else None
    total = cart.total()
    restaurant_names = sorted({i.menu_item.restaurant.name for i in items})
    if request.method == "POST":
        address = request.POST.get("delivery_address", "").strip()
        phone = request.POST.get("delivery_phone", "").strip()
        if not address:
            messages.error(request, "Please tell us where to bring your order (delivery address).")
        else:
            with transaction.atomic():
                created_orders = []
                if multiple_restaurants:
                    grouped = {}
                    for ci in items:
                        restaurant_key = ci.menu_item.restaurant
                        grouped.setdefault(restaurant_key, []).append(ci)
                    for restaurant_obj, restaurant_items in grouped.items():
                        order = Order.objects.create(
                            user=request.user,
                            restaurant=restaurant_obj,
                            status=Order.Status.PENDING_PAYMENT,
                            total=sum(ci.line_total() for ci in restaurant_items),
                            delivery_address=address,
                            delivery_phone=phone,
                            is_paid=False,
                        )
                        for ci in restaurant_items:
                            OrderItem.objects.create(
                                order=order,
                                menu_item=ci.menu_item,
                                name=ci.menu_item.name,
                                unit_price=ci.menu_item.price,
                                quantity=ci.quantity,
                            )
                        created_orders.append(order)
                else:
                    order = Order.objects.create(
                        user=request.user,
                        restaurant=restaurant,
                        status=Order.Status.PENDING_PAYMENT,
                        total=total,
                        delivery_address=address,
                        delivery_phone=phone,
                        is_paid=False,
                    )
                    for ci in items:
                        OrderItem.objects.create(
                            order=order,
                            menu_item=ci.menu_item,
                            name=ci.menu_item.name,
                            unit_price=ci.menu_item.price,
                            quantity=ci.quantity,
                        )
                    created_orders.append(order)
                cart.items.all().delete()
            if multiple_restaurants:
                first_order = created_orders[0]
                request.session["pending_payment_orders"] = [order.pk for order in created_orders]
                messages.success(
                    request,
                    "Orders placed for each restaurant. Complete one demo payment now and we will mark all the linked orders as paid.",
                )
                return redirect("payments:mock_pay", order_id=first_order.pk)
            messages.success(
                request,
                "Order placed! Next step: complete the demo checkout (no real money).",
            )
            return redirect("payments:mock_pay", order_id=order.pk)
    return render(
        request,
        "orders/checkout.html",
        {
            "items": items,
            "restaurant": restaurant,
            "total": total,
            "multiple_restaurants": multiple_restaurants,
            "restaurant_names": restaurant_names,
        },
    )


@login_required
def my_orders(request):
    profile = getattr(request.user, "profile", None)
    if profile and profile.role == Profile.Role.CUSTOMER:
        orders = Order.objects.filter(user=request.user).select_related("restaurant")
    else:
        orders = Order.objects.filter(
            restaurant__owner=request.user,
        ).select_related("restaurant", "user")
    return render(request, "orders/my_orders.html", {"orders": orders})


@login_required
def order_detail(request, pk):
    profile = getattr(request.user, "profile", None)
    if profile and profile.role == Profile.Role.CUSTOMER:
        order = get_object_or_404(Order, pk=pk, user=request.user)
    else:
        order = get_object_or_404(Order, pk=pk, restaurant__owner=request.user)
    status_choices = [
        c for c in Order.Status.choices if c[0] != Order.Status.PENDING_PAYMENT
    ]
    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
            "items": order.items.all(),
            "status_choices": status_choices,
        },
    )


@login_required
@require_http_methods(["POST"])
def owner_update_status(request, pk):
    profile = getattr(request.user, "profile", None)
    if not profile or profile.role != Profile.Role.OWNER:
        messages.error(request, "You can’t update that order.")
        return redirect("restaurant:home")
    order = get_object_or_404(Order, pk=pk, restaurant__owner=request.user)
    new_status = request.POST.get("status")
    valid = {c[0] for c in Order.Status.choices if c[0] != Order.Status.PENDING_PAYMENT}
    if order.status == Order.Status.PENDING_PAYMENT:
        messages.error(request, "Wait until the customer finishes demo payment before changing status.")
        return redirect("orders:detail", pk=pk)
    if new_status not in valid:
        messages.error(request, "That status isn’t valid — pick another option.")
        return redirect("orders:detail", pk=pk)
    order.status = new_status
    order.save(update_fields=["status", "updated_at"])
    messages.success(request, "Got it — we’ve updated the order status for the customer.")
    return redirect("orders:detail", pk=pk)
