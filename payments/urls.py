from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("mock/<int:order_id>/", views.mock_pay, name="mock_pay"),
]
