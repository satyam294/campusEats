from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=Profile.Role.choices,
        initial=Profile.Role.CUSTOMER,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("username", "email", "password1", "password2"):
            self.fields[name].widget.attrs.setdefault("class", "form-control")
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Confirm password"
        self.fields["role"].label = "You are signing up as"
        self.fields["phone"].label = "Phone (optional)"
        self.fields["phone"].help_text = "Handy if we need to reach you about your order."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if not commit:
            return user
        user.save()
        role = self.cleaned_data["role"]
        phone = self.cleaned_data.get("phone") or ""
        user.profile.role = role
        user.profile.phone = phone
        user.profile.save()
        return user
