from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "I want to order food"
        OWNER = "owner", "I run a campus outlet"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
