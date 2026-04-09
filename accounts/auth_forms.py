from django.contrib.auth.forms import AuthenticationForm


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if widget.__class__.__name__ in ("TextInput", "PasswordInput", "EmailInput"):
                widget.attrs.setdefault("class", "form-control")
