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
    if request.method == "POST":
        outcome = request.POST.get("outcome")
        tx = uuid.uuid4().hex
        if outcome == "success":
            Payment.objects.create(
                order=order,
                status=Payment.Status.SUCCESS,
                transaction_id=tx,
            )
            order.is_paid = True
            order.status = Order.Status.PLACED
            order.save(update_fields=["is_paid", "status", "updated_at"])
            messages.success(
                request,
                f"Payment went through (demo). Reference: {tx[:12]}… — the kitchen can start preparing.",
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
                "Demo payment didn’t go through — no worries, try again from your order page.",
            )
            return redirect("orders:detail", pk=order.pk)
    return render(request, "payments/mock_pay.html", {"order": order})
