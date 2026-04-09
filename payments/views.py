import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from orders.models import Order

from .models import Payment


@login_required
@require_http_methods(["GET", "POST"])
def mock_pay(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    if order.is_paid:
        messages.info(request, "You’re all set — this order is already paid.")
        return redirect("orders:detail", pk=order.pk)
    pending_ids = request.session.get("pending_payment_orders", [])
    group_payment = False
    group_total = None
    restaurant_names = None
    related_orders = None
    if pending_ids and order.pk in pending_ids:
        related_orders = Order.objects.filter(pk__in=pending_ids, user=request.user)
        if related_orders.count() > 1:
            group_payment = True
            group_total = sum(o.total for o in related_orders)
            restaurant_names = sorted({o.restaurant.name for o in related_orders})
    if request.method == "POST":
        outcome = request.POST.get("outcome")
        tx = uuid.uuid4().hex
        if outcome == "success":
            Payment.objects.create(
                order=order,
                status=Payment.Status.SUCCESS,
                transaction_id=tx,
            )
            if group_payment and related_orders is not None:
                for o in related_orders:
                    o.is_paid = True
                    o.status = Order.Status.PLACED
                    o.save(update_fields=["is_paid", "status", "updated_at"])
                del request.session["pending_payment_orders"]
                messages.success(
                    request,
                    f"Payment successful! Reference #{tx[:12].upper()} — all linked orders are now being prepared.",
                )
                return redirect("orders:mine")
            order.is_paid = True
            order.status = Order.Status.PLACED
            order.save(update_fields=["is_paid", "status", "updated_at"])
            messages.success(
                request,
                f"Payment successful! Reference #{tx[:12].upper()} — your order is now being prepared.",
            )
            return redirect("orders:detail", pk=order.pk)
        if outcome == "fail":
            Payment.objects.create(
                order=order,
                status=Payment.Status.FAILED,
                transaction_id=tx,
            )
            messages.warning(
                request,
                "Payment failed. Please try again or contact support if the issue persists.",
            )
            return redirect("orders:detail", pk=order.pk)
    return render(
        request,
        "payments/mock_pay.html",
        {
            "order": order,
            "group_payment": group_payment,
            "group_total": group_total,
            "restaurant_names": restaurant_names,
        },
    )
