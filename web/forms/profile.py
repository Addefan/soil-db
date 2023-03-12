from django import forms
from django.contrib.auth.hashers import make_password

from web.models import Staff


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields["email"].widget.attrs["readonly"] = ""
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            visible.field.widget.attrs["placeholder"] = "placeholder"

    class Meta:
        model = Staff
        widgets = {"email": forms.EmailInput()}
        fields = ("surname", "name", "email")
        readonly_fields = ("email",)
