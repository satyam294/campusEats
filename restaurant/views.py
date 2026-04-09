from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from accounts.models import Profile

from .forms import MenuItemForm, RestaurantForm
from .models import MenuItem, Restaurant


def home(request):
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(request, "restaurant/home.html", {"restaurants": restaurants})


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, is_active=True)
    items = restaurant.menu_items.filter(is_available=True)
    return render(
        request,
        "restaurant/detail.html",
        {"restaurant": restaurant, "items": items},
    )


def owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        profile = getattr(request.user, "profile", None)
        if not profile or profile.role != Profile.Role.OWNER:
            messages.error(request, "That area is for campus outlet managers.")
            return redirect("restaurant:home")
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
@owner_required
@require_http_methods(["GET", "POST"])
def my_restaurant(request):
    restaurant = getattr(request.user, "owned_restaurant", None)
    if request.method == "POST":
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            r = form.save(commit=False)
            r.owner = request.user
            r.save()
            messages.success(request, "Looking good — outlet details saved.")
            return redirect("restaurant:my_restaurant")
    else:
        form = RestaurantForm(instance=restaurant)
    return render(
        request,
        "restaurant/my_restaurant.html",
        {"form": form, "restaurant": restaurant},
    )


@login_required
@owner_required
@require_http_methods(["GET", "POST"])
def menu_item_create(request):
    restaurant = getattr(request.user, "owned_restaurant", None)
    if not restaurant:
        messages.warning(request, "Set up your outlet first — name, address, and a short blurb.")
        return redirect("restaurant:my_restaurant")
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()
            messages.success(request, "New dish added — students will see it on your menu.")
            return redirect("restaurant:menu_manage")
    else:
        form = MenuItemForm()
    return render(request, "restaurant/menu_item_form.html", {"form": form, "title": "Add a new dish"})


@login_required
@owner_required
def menu_manage(request):
    restaurant = getattr(request.user, "owned_restaurant", None)
    if not restaurant:
        messages.warning(request, "Set up your outlet first — name, address, and a short blurb.")
        return redirect("restaurant:my_restaurant")
    items = restaurant.menu_items.all()
    return render(
        request,
        "restaurant/menu_manage.html",
        {"restaurant": restaurant, "items": items},
    )


@login_required
@owner_required
@require_http_methods(["GET", "POST"])
def menu_item_edit(request, pk):
    restaurant = getattr(request.user, "owned_restaurant", None)
    if not restaurant:
        return redirect("restaurant:my_restaurant")
    item = get_object_or_404(MenuItem, pk=pk, restaurant=restaurant)
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu updated.")
            return redirect("restaurant:menu_manage")
    else:
        form = MenuItemForm(instance=item)
    return render(
        request,
        "restaurant/menu_item_form.html",
        {"form": form, "title": "Edit dish", "item": item},
    )


@login_required
@owner_required
@require_http_methods(["POST"])
def menu_item_delete(request, pk):
    restaurant = getattr(request.user, "owned_restaurant", None)
    if not restaurant:
        return redirect("restaurant:my_restaurant")
    item = get_object_or_404(MenuItem, pk=pk, restaurant=restaurant)
    item.delete()
    messages.success(request, "That dish has been removed from your menu.")
    return redirect("restaurant:menu_manage")
